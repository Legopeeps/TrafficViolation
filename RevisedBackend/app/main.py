from fastapi import FastAPI, Depends, HTTPException, status

# Added CORS middleware for Assignment 3
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError

# For parsing form data in the /token endpoint
from fastapi.security import OAuth2PasswordRequestForm

from . import models, schemas, auth
from .database import get_db

# Assessment Item 1: Database Design & Implementation (API Endpoint Development with vague implementation of Authentication)
# Note: Authentication is partially implemented but not fully integrated into all endpoints
# Module: CMP2812 Full Stack Development
# By Jack Stiller, 25788983

app = FastAPI(
    title="New York State System - API Solution by Jack Stiller (25788983)",
    version="1.0.0",
    description="A FastAPI application for managing traffic violation data in New York State. "
    "This API allows for authentication, driver and vehicle management, and violation notice handling, through using the database I created in Assignment 1."
    " Developed as part of the CMP2812 Full Stack Development module.")

# explicitly defined allowed origins, improved security by limiting access
# This is instead of allowing all with "allow_origins=["*"]"
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:9000",
    "http://localhost:9000",
    "http://127.0.0.1:3306",
    "http://localhost:3306",
]

# Add CORS middleware (Assignment 3 req.),
# allowing for data to be shared across addresses within "origins" list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. AUTHENTICATION ENDPOINTS (Token-focussed endpoints) ---

# For assignment three, @app.post("/token") has been updated
# as before only officers could log in.
# Currently, any user can log in through the same endpoint,
# differentiated by role


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    # Allows for form data parsing of username and password with Authorise on Swagger UI
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Note: OAuth2PasswordRequestForm uses .username and .password fields
    user = db.query(models.Officer).filter(
        models.Officer.officer_name == form_data.username).first()
    role = "officer"

    # If not found, check if they are a Driver
    if not user:
        user = db.query(models.Driver).filter(
            models.Driver.surname == form_data.username).first()
        role = "driver"

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Include the 'role' in the token so the frontend knows which dashboard to show
    access_token = auth.create_access_token(
        data={"sub": form_data.username, "role": role})

    return {"access_token": access_token, "token_type": "bearer"}


@app.put("/token", response_model=schemas.Token)
def refresh_token(current_user: str = Depends(auth.get_current_user)):
    """PUT /token: Refresh an existing valid token to extend the session"""
    access_token = auth.create_access_token(data={"sub": current_user})
    return {"access_token": access_token, "token_type": "bearer"}


@app.delete("/token")
def logout(current_user: str = Depends(auth.get_current_user)):
    """DELETE /token: Client-side logout confirmation"""
    return {"message": f"Successfully logged out {current_user}. Please delete your local token."}


# --- 2. GET ENDPOINTS (Three Required) ---
# Note: Added the get("officers/stats") endpoint for officers to retieve all violation notices

@app.get("/violations/", response_model=List[schemas.ViolationNotice])
def read_all_violations(db: Session = Depends(get_db)):
    """Returns all violations (No parameters required)"""
    return db.query(models.ViolationNotice).all()


@app.get("/drivers/{driver_id}", response_model=schemas.Driver)
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    """Returns a specific driver by ID (Contains parameter)"""
    driver = db.query(models.Driver).filter(
        models.Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@app.get("/officers/{personal_number}/notices", response_model=List[schemas.ViolationNotice])
def read_officer_notices(personal_number: int, db: Session = Depends(get_db)):
    """Returns notices issued by a specific officer (Contains parameter)"""
    return db.query(models.ViolationNotice).filter(
        models.ViolationNotice.personal_number == personal_number).all()


@app.get("/officers/stats")
def get_system_stats(db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    total_violations = db.query(models.ViolationNotice).count()
    total_drivers = db.query(models.Driver).count()

    # violation_stats will return a list of tuples like [(asleep_while_driving, 10), (speeding, 25), ...]
    # showing the count of each violation type
    violation_stats = db.query(models.ViolationNotice.violation_type, func.count(
    )).group_by(models.ViolationNotice.violation_type).all()
    return {
        "total_violations": total_violations,
        "total_drivers": total_drivers,
        "violation_stats": violation_stats
    }


# --- 3. POST ENDPOINTS (Two Required) ---

@app.post("/drivers/", response_model=schemas.Driver, status_code=201)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db),
                  current_user=Depends(auth.get_current_user)):
    """Add a new driver to the system (Protected)"""
    try:
        db_driver = models.Driver(**driver.model_dump())
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return db_driver
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Conflict: A driver with this license number already exists in the New York State database."
        )


@app.post("/violations/", response_model=schemas.ViolationNotice, status_code=201)
def create_violation(violation: schemas.ViolationNoticeCreate, db: Session = Depends(get_db),
                     current_user=Depends(auth.get_current_user)):
    """Log a new violation notice (Protected)"""
    try:
        db_violation = models.ViolationNotice(**violation.model_dump())
        db.add(db_violation)
        db.commit()
        db.refresh(db_violation)
        return db_violation
    except IntegrityError:
        db.rollback()  # Resets the database state after the failed attempt, accounting for the data entered not being valid
        raise HTTPException(
            status_code=400,
            detail="Integrity Error: The vehicle registration or officer ID "
            "provided does not exist in the system."
        )


# --- 4. PUT ENDPOINTS (Two Required) ---

@app.put("/drivers/{driver_id}", response_model=schemas.Driver)
def update_driver(driver_id: int, updated_data: schemas.DriverUpdate, db: Session = Depends(get_db),
                  current_user=Depends(auth.get_current_user)):
    """Update driver information (Protected)"""
    db_driver = db.query(models.Driver).filter(
        models.Driver.driver_id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    try:
        for key, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(db_driver, key, value)

        db.commit()
        db.refresh(db_driver)
        return db_driver

    except IntegrityError:
        """Made use of IntegrityError to catch the unique constraint violation when trying 
        to update a driver's license details when linked to a Vehicle or Violation"""
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot update driver: This record is linked to an existing Vehicle or Violation."
        )


@app.put("/vehicles/{registration_number}", response_model=schemas.Vehicle)
def update_vehicle(registration_number: str, updated_data: schemas.VehicleUpdate,
                   db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    """Update existing vehicle info (Protected)"""
    db_vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.registration_number == registration_number).first()

    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    try:
        # exclude_unset=True means only provided fields are updated
        for key, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(db_vehicle, key, value)

        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Update failed: Referential integrity violation. "
            "Check linked Driver or Violation data within the database"
            "or contact support."
        )


# --- 5. DELETE ENDPOINTS (Two Required) ---

@app.delete("/violations/{violation_id}")
def delete_violation(violation_id: int, db: Session = Depends(get_db),
                     current_user=Depends(auth.get_current_user)):
    """Delete a violation record (Protected)"""
    db_violation = db.query(models.ViolationNotice).filter(
        models.ViolationNotice.violation_ID == violation_id).first()
    if not db_violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    db.delete(db_violation)
    db.commit()
    return {"message": f"Violation {violation_id} successfully deleted by {current_user}"}


@app.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db),
                  current_user=Depends(auth.get_current_user)):
    """Delete a driver record (Protected)"""
    db_driver = db.query(models.Driver).filter(
        models.Driver.driver_id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    db.delete(db_driver)
    db.commit()
    return {"message":
            f"Driver {db_driver.forename} {db_driver.surname} successfully deleted by {current_user}"}
