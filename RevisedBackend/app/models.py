from sqlalchemy import Column, Integer, String, Date, Time, Numeric, ForeignKey, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .database import Base

# Assessment Item 1: Database Design & Implementation (SQLAlchemy Models)
# Module: CMP2812 Full Stack Development
# By Jack Stiller, 25788983


class Officer(Base):
    """
    Officer Table: personal_number is the Primary Key.
    """
    __tablename__ = "Officer"

    personal_number = Column(Integer, primary_key=True, nullable=False)
    officer_name = Column(String(100), nullable=False)

    # Relationship to Violation Notices
    notices = relationship("ViolationNotice", back_populates="officer")


class Driver(Base):
    """
    Driver Table: driver_id is the Primary Key.
    Includes a unique constraint on license and state to support composite FKs.
    """
    __tablename__ = "Driver"

    driver_id = Column(Integer, primary_key=True, nullable=False)
    forename = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    address = Column(String(150))
    city = Column(String(50))
    state = Column(String(2), nullable=False)
    drivers_license = Column(String(20), nullable=False, unique=True)
    drivers_license_state = Column(String(2), nullable=False)
    date_of_birth = Column(Date)
    height = Column(Numeric(4, 1))
    weight = Column(Numeric(5, 2))
    eye_colour = Column(String(20))

    # Unique constraint to ensure no duplicate licenses if logged across multiple American states
    __table_args__ = (
        UniqueConstraint("drivers_license_state",
                         "drivers_license", name="uk_license"),  # uk = unique key not "united kingdom" license
    )


class Vehicle(Base):
    """
    Vehicle Table: registration_number is the Primary Key.
    Uses a Composite ForeignKeyConstraint to link to Driver's license details.
    """
    __tablename__ = "Vehicle"

    registration_number = Column(String(10), primary_key=True, nullable=False)
    colour = Column(String(30))
    make = Column(String(50))
    VIN = Column(String(17), unique=True)
    address = Column(String(150))
    drivers_license_state = Column(String(2), nullable=False)
    drivers_license = Column(String(20), nullable=False)
    # in "year", integer is used to allow for easier sorting
    year = Column(Integer)
    type = Column(String(30))
    registered_owner = Column(String(100))

    # Composite Foreign Key referencing Driver
    __table_args__ = (
        ForeignKeyConstraint(
            ["drivers_license_state", "drivers_license"],
            ["Driver.drivers_license_state", "Driver.drivers_license"],
            name="fk_driver_license"
        ),
    )

    notices = relationship("ViolationNotice", back_populates="vehicle")


class ViolationNotice(Base):
    """
    Violation_Notice Table: violation_ID is the Primary Key.
    """
    __tablename__ = "Violation_Notice"

    violation_ID = Column(Integer, primary_key=True, nullable=False)
    personal_number = Column(Integer, ForeignKey(
        "Officer.personal_number"), nullable=False)
    registration_number = Column(String(10), ForeignKey(
        "Vehicle.registration_number"), nullable=False)
    violation_type = Column(String(100), nullable=False)
    violation_date = Column(Date, nullable=False)
    violation_time = Column(Time)
    district = Column(String(50))
    detachment = Column(String(50))
    location = Column(String(150))

    # Relationships
    officer = relationship("Officer", back_populates="notices")
    vehicle = relationship("Vehicle", back_populates="notices")
