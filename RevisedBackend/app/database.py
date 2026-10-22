import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Assessment Item 1: Database Design & Implementation (Database Connection Setup and Session Management)
# Module: CMP2812 Full Stack Development
# By Jack Stiller, 25788983

"""using the variables from the dockerfile, but with defaults for local testing"""
DB_USER = os.getenv("USERNAME", "root")
DB_PASS = os.getenv("PASSWORD", "")
DB_HOST = os.getenv("HOST", "127.0.0.1")
DB_PORT = os.getenv("PORT", "3306")
DB_NAME = "TrafficViolationsDB"

"""Database connection URL for MySQL using mysqlconnector driver
   Note: root = username, password is empty"""
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creates the engine to talk to MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # to be derived in models.py


def get_db():  # get_db is for using API endpoints to get a database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
