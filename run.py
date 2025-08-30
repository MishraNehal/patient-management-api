#!/usr/bin/env python3
"""
Simple FastAPI Patient Management System Runner
"""

import uvicorn
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app

if __name__ == "__main__":
    print("🚀 Starting Patient Management System API...")
    print("📚 API Documentation will be available at: http://localhost:8000/docs")
    print("📖 ReDoc Documentation will be available at: http://localhost:8000/redoc")
    print("🌐 API will be running at: http://localhost:8000")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
