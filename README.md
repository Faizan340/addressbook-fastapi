# FastAPI Address Book Application (Async)

## Overview
This is a **RESTful API** built using **FastAPI** and **Python 3**, demonstrating modern backend development practices including **asynchronous database operations**.  

The application manages **addresses with geographic coordinates (latitude and longitude)** and supports **distance-based queries**. All database operations are **fully async** using **SQLAlchemy Async ORM** for better performance and scalability.

The application does **not have a GUI**; you can explore and test APIs using FastAPI's built-in **Swagger UI**.

---

## Features
- **Async CRUD Operations**
  - Create, update, delete, and retrieve addresses
  - Fully asynchronous database operations using `AsyncSession`
- **Geospatial Queries**
  - Find addresses within a specified distance from given coordinates
  - Distance calculation using the **Haversine formula**
- **Database**
  - SQLite database for persistence
  - SQLAlchemy Async ORM for data access
- **Validation**
  - Input data validated using **Pydantic schemas**
- **Error Handling**
  - Returns proper HTTP error codes for missing or invalid data
- **Dependency Injection**
  - Uses FastAPI `Depends` for clean async session management

---

## Tech Stack
- **Python 3.10+**
- **FastAPI** (async support)
- **SQLAlchemy Async ORM**
- **SQLite**
- **Pydantic**
- **Uvicorn** (ASGI server)

---

## Setup and Execution

### 1. Clone and setup
git clone https://github.com/Faizan340/addressbook-fastapi.git

cd addressbook-fastapi

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

### 2. Run the application
uvicorn app.main:app --reload

### 3. Access the API
Open your browser to the interactive documentation: http://127.0.0.1:8000/docs

## API Endpoints

1. POST /addresses - Create a new address
2. GET /addresses/{address_id} - Retrieve specific address
3. PUT /addresses/{address_id} - Update an address
4. DELETE /addresses/{address_id} - Delete an address
5. GET /addresses/nearby/ - Find addresses within distance

## Usage Example
# Create An address post
Endpoint: /addresses/ Sample JSON Payload:

{
  "name": "Indiranagar",
  "latitude": 12.9784,
  "longitude": 77.6408
}

# Find Nearby Addresses (GET)
Endpoint: /addresses/nearby/ Parameters:

latitude: 37.7750
longitude: -122.4180
distance_km: 5.0

----------------------




