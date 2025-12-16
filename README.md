# Movies ETL Pipeline

## Overview

This project implements an **ETL (Extract, Transform, Load) pipeline** for processing a Movies dataset. The pipeline reads data from a CSV file, cleans and transforms it, and loads it into a **normalized PostgreSQL schema** using SQLAlchemy ORM.

The project uses a staging table to load raw CSV data, which is then transformed into typed fields and normalized tables.
String arrays and JSON-like columns are parsed and expanded into separate tables, connected to movies through many-to-many relationships, reflecting real-world data engineering workflows.

---

## Technologies

- Python 3.x
- Pandas
- SQLAlchemy ORM
- PostgreSQL

---

## Project Structure

```text

-> main.py               # Entry point for ETL process
-> db.py                 # Database configuration and session
-> models.py             # SQLAlchemy models
-> crud.py               # CRUD functions, including get_or_create_fields
-> transforms.py         # Transformations and ETL logic
-> requirements.txt      # Python dependencies
-> data/                 # Folder with CSV files
-> README.md             # This file

## Database Models

### Main Tables

- **MovieStaging** – staging table for initial CSV load
- **Movie** – main movies table
- **Genre** – normalized genre reference table
- **Keyword** – normalized keyword reference table
- **Cast** – normalized cast/actor reference table
- **ProductionCompany** – normalized production companies
- **ProductionCountry** – normalized production countries
- **SpokenLanguage** – normalized spoken languages
- **Crew** – normalized crew members

---

### Many-to-Many Tables

- **MovieGenre**
- **MovieKeyword**
- **MovieCast**
- **MovieProductionCompany**
- **MovieProductionCountry**
- **MovieSpokenLanguage**
- **MovieCrew**

These tables manage the relationships between movies and their associated attributes.

---

## ETL Process

### 1. Extract

- CSV file → Pandas DataFrame → **MovieStaging** table

---

### 2. Clean

- Normalize `None`, `NaN`, `NaT` values
- Convert `release_date` to a proper date or `None`
- Convert all other non-string or invalid values to empty strings

---

### 3. Transform

- Parse and transform columns into separate normalized tables
- Convert cleaned string values to appropriate types (int, float, date) during model assignment
- Deduplicate records using `get_or_create_fields`
- Maintain referential integrity between tables

---

### 4. Load

- Load transformed data into main tables
- Populate many-to-many association tables

---

## Idempotency

The ETL pipeline is **idempotent**:

- Tables are created only if they do not exist
- Reference records are checked before insertion
- Many-to-many relationships are added only if missing

This allows safe repeated execution without creating duplicate records.
