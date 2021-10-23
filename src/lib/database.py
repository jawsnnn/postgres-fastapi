"""
Library for database functions
22-Oct-2021
"""

import os

def construct_db_url() -> str:
    """
    Constructs a database url from environment variables
    """
    database_name = os.environ.get("DATABASE_NAME")
    db_host_name = os.environ.get("DATABASE_HOST_NAME")
    user_name = os.environ.get("DATABASE_USER")
    password = os.environ.get("DATABASE_PASSWORD")
    port_number = os.environ.get("DATABASE_PORT")
    return f"postgresql+asyncpg://{user_name}:{password}@{db_host_name}:{port_number}/{database_name}"