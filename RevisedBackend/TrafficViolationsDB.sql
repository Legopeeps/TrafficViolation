#######################################################################
# header comment
# Assessment Item 1: Database Design & Implementation (Part 2 - .sql Script)
# Module: CMP2812 Full Stack Development
# By Jack Stiller, 25788983
#######################################################################

# Database setup
-- Drops the database if it exists to ensure a fresh, clean execution
DROP DATABASE IF EXISTS TrafficViolationsDB;

-- Creates the new database
CREATE DATABASE TrafficViolationsDB;

-- Selects the above created database explicitly
USE TrafficViolationsDB;

# Data Definition Language (DDL) - Creating the tables within the database
-- Primary Keys (PK) and Foreign Keys (FK) are defined based on the ERD.

# Officer Table
-- personal_number is the Primary Key.
CREATE TABLE Officer (
    personal_number INT NOT NULL,
    officer_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (personal_number)
);

# Driver Table
-- driver_id is the Primary Key.
-- The composite key (drivers_license_state, drivers_license) is made UNIQUE
-- to support the Foreign Key reference from the Vehicle table as per the ERD.
CREATE TABLE Driver (
    driver_id INT NOT NULL,
    forename VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    address VARCHAR(150),
    city VARCHAR(50),
    state CHAR(2) NOT NULL,
    drivers_license VARCHAR(20) NOT NULL UNIQUE, 
    drivers_license_state CHAR(2) NOT NULL,
    date_of_birth DATE,
    height DECIMAL(4,1),
    weight DECIMAL(5,2),
    eye_colour VARCHAR(20),
    PRIMARY KEY (driver_id),

    #Unique constraint which is needed to reference from the Vehicle table
    UNIQUE KEY uk_license (drivers_license_state, drivers_license)
);

# Vehicle Table
-- registration_number is the Primary Key.
-- FK references a driver based on their license details.
CREATE TABLE Vehicle (
    registration_number VARCHAR(10) NOT NULL,
    colour VARCHAR(30),
    make VARCHAR(50),
    VIN VARCHAR(17) UNIQUE,
    address VARCHAR(150),
    drivers_license_state CHAR(2) NOT NULL,
    drivers_license VARCHAR(20) NOT NULL,
    year YEAR,
    type VARCHAR(30),
    registered_owner VARCHAR(100),
    PRIMARY KEY (registration_number),
    -- Composite Foreign Key to Driver table
    CONSTRAINT fk_driver_license
        FOREIGN KEY (drivers_license_state, drivers_license)
        REFERENCES Driver (drivers_license_state, drivers_license)
);

# Violation_Notice Table
-- violation_ID is the Primary Key.
-- Contains Foreign Keys to Officer and Vehicle tables.
CREATE TABLE Violation_Notice (
    violation_ID INT NOT NULL,
    personal_number INT NOT NULL,       -- FK to Officer
    registration_number VARCHAR(10) NOT NULL, -- FK to Vehicle
    violation_type VARCHAR(100) NOT NULL,
    violation_date DATE NOT NULL,
    violation_time TIME,
    district VARCHAR(50),
    detachment VARCHAR(50),
    location VARCHAR(150),
    PRIMARY KEY (violation_ID),
    FOREIGN KEY (personal_number) REFERENCES Officer(personal_number),
    FOREIGN KEY (registration_number) REFERENCES Vehicle(registration_number)
);


# Data Control Language(DCL) - User Crreation
-- Creates users and assigns privileges based on the basic Role-Based Access rule within the breif:
-- 	Citizen can only view notices linked to their vehicle.
--  Officers can create new notices (and presumably view/update their own).

-- Drops users if they already exist to prevent errors
DROP USER IF EXISTS 'officer_user'@'localhost';
DROP USER IF EXISTS 'citizen_user'@'localhost';

# Officer Role: Can INSERT (create) notices, and SELECT/UPDATE on other tables
CREATE USER 'officer_user'@'localhost' IDENTIFIED BY 'OfficerPass123';
GRANT SELECT, INSERT, UPDATE ON TrafficViolationsDB.Violation_Notice TO 'officer_user'@'localhost';
GRANT SELECT ON TrafficViolationsDB.Officer TO 'officer_user'@'localhost';
GRANT SELECT ON TrafficViolationsDB.Driver TO 'officer_user'@'localhost';
GRANT SELECT ON TrafficViolationsDB.Vehicle TO 'officer_user'@'localhost';

# Citizen Role: Can only SELECT (view) data
CREATE USER 'citizen_user'@'localhost' IDENTIFIED BY 'CitizenPass123';
GRANT SELECT ON TrafficViolationsDB.Violation_Notice TO 'citizen_user'@'localhost';
GRANT SELECT ON TrafficViolationsDB.Driver TO 'citizen_user'@'localhost';
GRANT SELECT ON TrafficViolationsDB.Vehicle TO 'citizen_user'@'localhost';

FLUSH PRIVILEGES;


# Data Manipulation Language(DML) - Inserting Data, populating the tables with (in this case) placeholder values to demonstrate functionality

# Officer Data
INSERT INTO Officer (personal_number, officer_name) VALUES
(1001, 'Sergeant John Smith'),
(1002, 'Officer Jane Doe'),
(1003, 'Constable Alex Lee');

# Driver Data
INSERT INTO Driver (driver_id, forename, surname, address, city, state, drivers_license, drivers_license_state, date_of_birth, height, weight, eye_colour) VALUES
(201, 'Michael', 'Johnson', '123 Oak St', 'Raleigh', 'NC', 'NC12345', 'NC', '1985-05-15', 178.5, 75.20, 'Brown'),
(202, 'Emily', 'Bleeper', '45 Pine Ave', 'Durham', 'NC', 'NC67890', 'NC', '1992-10-20', 165.0, 58.90, 'Blue'),
(203, 'David', 'Garcia', '78 Maple Rd', 'Charlotte', 'NC', 'NC11223', 'NC', '1970-02-28', 185.3, 90.10, 'Green'),
(204, 'Jessica', 'Wonge', '101 Bay St', 'Raleigh', 'NC', 'NC44556', 'NC', '2004-12-01', 168.0, 62.00, 'Hazel');

# Vehicle Data
INSERT INTO Vehicle (registration_number, colour, make, VIN, address, drivers_license_state, drivers_license, year, type, registered_owner) VALUES
('ABC-123', 'Orange', 'Toyota', 'JT1A1FEXL12345678', '123 Oak St', 'NC', 'NC12345', '2018', 'Sedan', 'Michael Johnson'),
('XYZ-987', 'Blue', 'Honda', '3C3C0AAS0A9876543', '45 Pine Ave', 'NC', 'NC67890', '2020', 'SUV', 'Emily Brown'),
('DEF-456', 'Black', 'Ford', '1FMYU7M20J1112233', '78 Maple Rd', 'NC', 'NC11223', '2015', 'Truck', 'David Garcia'),
('WXY-789', 'Silver', 'Vauxhall', 'JNYC45B3XU2121000', '101 Bay St', 'NC', 'NC44556', '2023', 'Hatchback', 'Jessica Wonge'); 

# Violation Notice Data
INSERT INTO Violation_Notice (violation_ID, personal_number, registration_number, violation_type, violation_date, violation_time, district, detachment, location) VALUES
(1, 1001, 'ABC-123', 'Speeding (15 mph over limit)', '2025-10-01', '10:30:00', 'Central', 'A-Unit', 'I-40 West'),
(2, 1002, 'XYZ-987', 'Failure to stop at a red light', '2025-10-05', '15:45:00', 'North', 'B-Unit', 'Hillsborough St & Gorman St'),
(3, 1001, 'DEF-456', 'Expired Registration', '2025-10-10', '08:00:00', 'South', 'C-Unit', 'US-1 South'),
(4, 1003, 'WXY-789', 'Illegal use of mobile phone while driving', '2025-10-11', '11:00:00', 'Central', 'A-Unit', 'NC-54 west'),
(5, 1002, 'ABC-123', 'Vehicle light not operating correctly', '2025-05-15', '19:20:00', 'West', 'D-Unit', 'US-70 East'),
(6, 1003, 'ABC-123', 'Speeding (15 mph over limit)', '2025-10-04', '21:05:00', 'Central', 'A-Unit', 'I-40 West'),
(7, 1002, 'XYZ-987', 'Vehicle light not operating correctly', '2025-05-16', '19:20:00', 'West', 'D-Unit', 'US-70 East');