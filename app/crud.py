"""
Database access layer for Address entities.
Contains all persistence and query logic.
"""

from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import calculate_distance_km


def create_address(db: Session, data: schemas.AddressCreate):
    address = models.Address(
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(db: Session, address_id: int, data: schemas.AddressUpdate):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not address:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, address_id: int) -> bool:
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not address:
        return False

    db.delete(address)
    db.commit()
    return True


def get_addresses_within_distance(
    db: Session,
    latitude: float,
    longitude: float,
    distance_km: float,
):
    addresses = db.query(models.Address).all()
    results = []

    for address in addresses:
        if address.latitude is None or address.longitude is None:
            continue

        distance = calculate_distance_km(
            latitude,
            longitude,
            address.latitude,
            address.longitude,
        )

        if distance <= distance_km:
            results.append(address)

    return results
