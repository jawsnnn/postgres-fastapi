from fastapi import FastAPI, status

from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from lib.database import create_database
from lib.database import construct_db_url
from lib.database import create_engine

app = FastAPI(title = "Demo FastAPI app running on postgresql")

load_dotenv()

db_url = construct_db_url()

database = create_database(db_url)

engine = create_engine(db_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    '''
    Startup the app by connecting to the database
    '''
    database.connect()