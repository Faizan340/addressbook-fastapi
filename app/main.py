from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, AsyncSessionLocal, Base
from app import schemas, crud
from app.logging_config import logger
import contextlib

# Lifecycle to create tables on startup
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="AddressBook API", lifespan=lifespan)

# Dependency Injection
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

@app.post("/addresses", response_model=schemas.AddressResponse)
async def create_address(data: schemas.AddressCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Creating address")
    return await crud.create_address(db, data)

@app.put("/addresses/{address_id}", response_model=schemas.AddressResponse)
async def update_address(address_id: int, data: schemas.AddressUpdate, db: AsyncSession = Depends(get_db)):
    address = await crud.update_address(db, address_id, data)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.delete("/addresses/{address_id}")
async def delete_address(address_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_address(db, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}

@app.get("/addresses/nearby", response_model=list[schemas.AddressResponse])
async def get_nearby_addresses(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: AsyncSession = Depends(get_db),
):
    # Ensure you updated crud.get_addresses_within_distance to be async
    return await crud.get_addresses_within_distance(
        db, latitude, longitude, distance_km
    )
