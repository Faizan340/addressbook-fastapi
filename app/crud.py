from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate
from app.utils import calculate_distance_km


# CREATE (Async)
async def create_address(
    db: AsyncSession,
    data: AddressCreate
) -> Address:
    address = Address(**data.dict())
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


# READ / UPDATE / DELETE helpers (Async)
async def get_address(db: AsyncSession, address_id: int):
    # Note: .query() is replaced by execute(select(...))
    result = await db.execute(select(Address).filter(Address.id == address_id))
    return result.scalars().first()

async def update_address(
    db: AsyncSession,
    address_id: int,
    data: AddressUpdate
) -> Optional[Address]:
    result = await db.execute(
        select(Address).where(Address.id == address_id)
    )
    address = result.scalar_one_or_none()

    if not address:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(address, field, value)

    await db.commit()
    await db.refresh(address)
    return address


async def delete_address(
    db: AsyncSession,
    address_id: int
) -> bool:
    result = await db.execute(
        select(Address).where(Address.id == address_id)
    )
    address = result.scalar_one_or_none()

    if not address:
        return False

    await db.delete(address)
    await db.commit()
    return True


# GEOSPATIAL SEARCH (Async)
async def get_addresses_within_distance(
    db: AsyncSession,
    latitude: float,
    longitude: float,
    distance_km: float
) -> List[Address]:

    result = await db.execute(select(Address))
    addresses = result.scalars().all()

    return [
        addr
        for addr in addresses
        if calculate_distance_km(
            latitude,
            longitude,
            addr.latitude,
            addr.longitude
        ) <= distance_km
    ]
