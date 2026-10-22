from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional
from decimal import Decimal

# Assessment Item 1: Database Design & Implementation (Pydantic Schemas)
# Module: CMP2812 Full Stack Development
# By Jack Stiller, 25788983


class ORMBase(BaseModel):
    """Base class, saves writing a config class for each schema """
    class Config:
        # Allows Pydantic to read data from SQLAlchemy models using attribute access
        from_attributes = True


# --- AUTHENTICATION ---


class Token(BaseModel):
    access_token: str
    token_type: str


# --- OFFICER SCHEMAS ---


class OfficerBase(BaseModel):
    personal_number: int
    officer_name: str


class OfficerCreate(OfficerBase):
    pass


class Officer(OfficerBase, ORMBase):
    pass

# --- DRIVER SCHEMAS ---


class DriverBase(BaseModel):
    driver_id: int
    forename: str
    surname: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: str = Field(..., max_length=2)
    drivers_license: str
    drivers_license_state: str = Field(..., max_length=2)
    date_of_birth: Optional[date] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    eye_colour: Optional[str] = None


class DriverCreate(DriverBase):
    pass


class Driver(DriverBase, ORMBase):
    pass


class DriverUpdate(BaseModel):
    forename: Optional[str] = None
    surname: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None

# --- VEHICLE SCHEMAS ---


class VehicleBase(BaseModel):
    registration_number: str
    colour: Optional[str] = None
    make: Optional[str] = None
    VIN: Optional[str] = None
    address: Optional[str] = None
    drivers_license_state: str
    drivers_license: str
    year: Optional[int] = None
    type: Optional[str] = None
    registered_owner: Optional[str] = None


class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase, ORMBase):
    pass


class VehicleUpdate(BaseModel):
    colour: Optional[str] = None
    make: Optional[str] = None
    registered_owner: Optional[str] = None

# --- VIOLATION NOTICE SCHEMAS ---


class ViolationNoticeBase(BaseModel):
    violation_ID: int
    personal_number: int
    registration_number: str
    violation_type: str
    violation_date: date
    violation_time: Optional[time] = None
    district: Optional[str] = None
    detachment: Optional[str] = None
    location: Optional[str] = None


class ViolationNoticeCreate(ViolationNoticeBase):
    pass


class ViolationNotice(ViolationNoticeBase, ORMBase):

    officer: Optional[Officer] = None
    vehicle: Optional[Vehicle] = None
