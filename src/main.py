from fastapi import FastAPI, status

from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from lib.database import create_database

app = FastAPI(title = "Demo FastAPI app running on postgresql")

load_dotenv()

database = create_database()



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