# Patient Management System API

A FastAPI-based patient management system that demonstrates CRUD operations, data validation, and automatic BMI calculation with health verdicts.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete patient records
- **Automatic BMI Calculation**: Computes BMI automatically from height and weight
- **Health Verdict System**: Provides health status based on BMI ranges
- **Data Validation**: Comprehensive input validation using Pydantic models
- **RESTful API**: Clean and intuitive API endpoints
- **JSON Storage**: Simple file-based data persistence
- **Sorting Capabilities**: Sort patients by weight, height, or BMI

## 🏗️ Project Structure

```
patient-management-api/
├── src/
│   └── main.py              # FastAPI application and endpoints
├── data/
│   └── patients.json        # Patient data storage
├── tests/
│   └── test_main.py         # Test cases for the API
├── requirements.txt          # Python dependencies
├── run.py                   # Simple application runner
└── README.md                # Project documentation
```

## 🛠️ Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd patient-management-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### 3. Run Tests (Optional)
```bash
pytest tests/ -v
```

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### Base Endpoints
- `GET /` - Welcome message
- `GET /about` - API information

### Patient Management
- `GET /view` - Get all patients
- `GET /view/{patient_id}` - Get specific patient by ID
- `POST /create` - Create new patient
- `PUT /edit/{patient_id}` - Update existing patient
- `DELETE /delete/{patient_id}` - Delete patient

### Utility Endpoints
- `GET /sort?sortby={field}&order={asc/desc}` - Sort patients by weight, height, or BMI

## 📊 Patient Data Model

```json
{
  "id": "P001",
  "name": "Patient Name",
  "city": "City Name",
  "age": 25,
  "gender": "male|female|others",
  "height": 1.75,
  "weight": 70.0,
  "bmi": 22.86,
  "verdict": "Normal weight"
}
```

### BMI Categories
- **Underweight**: BMI < 18.5
- **Normal weight**: BMI 18.5 - 24.9
- **Overweight**: BMI 25.0 - 29.9
- **Obesity**: BMI ≥ 30.0

## 💡 Usage Examples

### Create a New Patient
```bash
curl -X POST "http://localhost:8000/create" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "P006",
       "name": "Jane Smith",
       "city": "Boston",
       "age": 28,
       "gender": "female",
       "height": 1.68,
       "weight": 65.0
     }'
```

### Get All Patients
```bash
curl "http://localhost:8000/view"
```

### Sort Patients by BMI (Descending)
```bash
curl "http://localhost:8000/sort?sortby=bmi&order=desc"
```

## 🔧 Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server for running FastAPI applications
- **Python 3.8+** - Programming language
- **Pytest** - Testing framework

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy Coding! 🎉**
# patient-management-api
