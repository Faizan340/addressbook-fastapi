from pydantic import BaseModel, Field
from typing import Optional

class AddressBase(BaseModel):
    name: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class AddressCreate(AddressBase):
    """Schema for creating an address"""
    pass

class AddressUpdate(BaseModel):
    """Schema for updating an address (partial updates allowed)"""
    name: Optional[str] = Field(None, min_length=1)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class AddressResponse(AddressBase):
    """Schema for reading/response"""
    id: int

    model_config = {
        "from_attributes": True
    }
