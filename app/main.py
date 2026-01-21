"""
Application entry point.
Defines API routes and dependency injection.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import schemas, crud, models
from app.logging_config import logger


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses", response_model=schemas.AddressResponse)
def create_address(data: schemas.AddressCreate, db: Session = Depends(get_db)):
    logger.info("Creating address")
    return crud.create_address(db, data)

@app.put("/addresses/{address_id}", response_model=schemas.AddressResponse)
def update_address(address_id: int, data: schemas.AddressUpdate, db: Session = Depends(get_db)):
    address = crud.update_address(db, address_id, data)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    if not crud.delete_address(db, address_id):
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}

@app.get("/addresses/nearby", response_model=list[schemas.AddressResponse])
def get_nearby_addresses(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: Session = Depends(get_db),
):
    return crud.get_addresses_within_distance(
        db, latitude, longitude, distance_km
    )
