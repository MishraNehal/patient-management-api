from fastapi import FastAPI, Path, HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import os

# Function to load patient data from JSON file
def load_data():
    # Get the directory where main.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then into data folder
    data_path = os.path.join(os.path.dirname(current_dir), 'data', 'patients.json')
    
    with open(data_path, 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    # Get the directory where main.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then into data folder
    data_path = os.path.join(os.path.dirname(current_dir), 'data', 'patients.json')
    
    with open(data_path, 'w') as file:
        json.dump(data, file, indent=4)

# Create FastAPI instance
app = FastAPI(
    title="Patient Management System API",
    description="A comprehensive API for managing patient records with BMI calculation and health verdicts",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Patient Model
class Patient(BaseModel):
    id: Annotated[str, Field(...,
        title="Patient ID",
        description="The unique identifier of the patient (e.g., P001, P002)",
        json_schema_extra={"example": "P001"},
        pattern="^P\\d{3}$"
    )]
    name: Annotated[str, Field(..., description="Full name of the patient")]
    city: Annotated[str, Field(..., description="City of residence")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI"""
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """Return health verdict based on BMI"""
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female' , 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

# Root endpoint
@app.get("/")
def root():
    return {"message": "Patient Management System API"}

# About endpoint
@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

# Endpoint to view all patients
@app.get("/view")
def get_all_patients():
    patients = load_data()
    return patients

# Endpoint to view a specific patient by ID
@app.get("/view/{patient_id}")
def get_patient(patient_id: str = Path(..., title="Patient ID", description="Unique identifier", examples={"patient_id": {"summary": "Example patient ID", "value": "P001"}})):
    patients = load_data()
    if patient_id in patients:
        return patients[patient_id]
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")

# Endpoint to create a new patient
@app.post("/create")
def create_patient(patient: Patient):
    patients = load_data()
    if patient.id in patients:
        raise HTTPException(status_code=400, detail=f"Patient with ID {patient.id} already exists.")

    # Save patient data (including computed fields) as dictionary
    patients[patient.id] = patient.model_dump()
    save_data(patients)

    return JSONResponse(
        status_code=201,
        content={"message": f"Patient with ID {patient.id} created successfully.", "patient": patient.model_dump()}
    )

# Endpoint to sort patients
@app.get("/sort")
def sort_patients(sortby: str = Query("weight", title="Sort field", description="Field to sort by", examples={"sortby": {"summary": "Sort by weight", "value": "weight"}}), order: str = Query("asc", title="Sort order", description="Sort order (asc/desc)", examples={"order": {"summary": "Ascending order", "value": "asc"}})):
    valid_fields = {"weight", "height", "bmi"}
    valid_orders = {"asc", "desc"}
    if sortby not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field. Choose from weight, height, bmi.")
    if order not in valid_orders:
        raise HTTPException(status_code=400, detail="Invalid order value. Choose 'asc' or 'desc'.")

    patients = load_data()
    sorted_patients = sorted(
        patients.items(),
        key=lambda item: item[1][sortby],
        reverse=(order == "desc")
    )
    return [{"id": pid, **data} for pid, data in sorted_patients]


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str = Path(..., title="Patient ID", description="ID of patient to update", examples={"patient_id": {"summary": "Example patient ID", "value": "P001"}}), patient_update: PatientUpdate = None):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str = Path(..., title="Patient ID", description="ID of patient to delete", examples={"patient_id": {"summary": "Example patient ID", "value": "P001"}})):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})
