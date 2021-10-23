from os import putenv
from fastapi import FastAPI, status

from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from lib.database import create_database
from lib.database import construct_db_url
from lib.database import create_engine
from lib.database import create_tables
from lib.models import GetNote, PutNote

app = FastAPI(title = "Demo FastAPI app running on postgresql")

load_dotenv()

db_url = construct_db_url()

database = create_database(db_url)

engine = create_engine(db_url)

dict_tables = create_tables(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup() -> None:
    '''
    Startup the app by connecting to the database
    '''
    await database.connect()

@app.on_evnet("shutdown")
async def shutdown() -> None:
    '''
    Shutdown the app by closing the database connection
    '''
    await database.disconnect()

@app.post(
    "/notes/", 
    response_model = PutNote, 
    status_code = status.HTTP_201_CREATED)
async def create_note(note: PutNote) -> dict:
    '''
    Create a note
    '''
    notes = dict_tables.get("notes")
    query = notes.insert().values(text=note.text, completed = note.completed)
    note_id = await database.execute(query)
    return {**note.dict(), "id": note_id}

@app.put(
    "/notes/{note_id}",
    response_model = PutNote,
    status_code = status.HTTP_200_OK)
async def update_note(note_id: int, note: PutNote) -> dict:
    '''
    Update a note
    '''
    notes = dict_tables.get("notes")
    query = notes.update().where(notes.c.id == note_id).values(text=note.text, completed = note.completed)
    await database.execute(query)
    return {**note.dict(), "id": note_id}

@app.get(
    "/notes/",
    response_model = GetNote,
    status_code = status.HTTP_200_OK
    )
async def get_notes(skip: int=0, limit: int = 20) -> list:
    '''
    Get all notes
    '''
    notes = dict_tables.get("notes")
    query = notes.select().offset(skip).limit(limit)
    return await database.fetch_all(query)

@app.get(
    "/notes/{note_id}",
    response_model = GetNote,
    status_code = status.HTTP_200_OK
    )
async def get_ntoe(note_id: int) -> GetNote:
    '''
    Get a note
    '''
    notes = dict_tables.get("notes")
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)

@app.delete(
    "/notes/{note_id}",
    status_code = status.HTTP_200_OK
    )
async def delete_note(note_id: int) -> dict:
    notes = dict_tables.get("notes")
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {'message': f'Message with id {note_id} deleted'}
