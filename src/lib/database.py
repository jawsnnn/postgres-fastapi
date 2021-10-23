"""
Library for database functions
22-Oct-2021
"""

import os
from typing import Protocol
import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()

def construct_db_url() -> str:
    """
    Constructs a database url from environment variables
    """
    database_name = os.environ.get("DATABASE_NAME")
    db_host_name = os.environ.get("DATABASE_HOST_NAME")
    user_name = os.environ.get("DATABASE_USER")
    password = os.environ.get("DATABASE_PASSWORD")
    port_number = os.environ.get("DATABASE_PORT")
    ssl_mode = os.environ.get("DATABASE_SSL_MODE")
    return f"postgresql://{user_name}:{password}@{db_host_name}:{port_number}/{database_name}?ssl_mode={ssl_mode}"    
    
def create_database(db_url : str) -> databases.Database:
    """
    Creates a database
    """
    database = databases.Database(db_url)

    return database


engine = sqlalchemy.create_engine(
    construct_db_url(), 
    pool_size=3,
    max_overflow=0)

metadata.create_all(engine)

# Tables
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String(255)),
    sqlalchemy.Column("completed"), sqlalchemy.Boolean
)
