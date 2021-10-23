# pylint: disable=import-error
'''
FastAPI postgresql backend
'''
from typing import List

from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
import databases
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from .lib.database import construct_db_url
from .models.notes import GetNote, PutNote

load_dotenv()

db_url = construct_db_url()

print(db_url)

database = databases.Database(db_url)

engine = create_async_engine(
    db_url, echo = True)


metadata = sqlalchemy.MetaData()

# Tables
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String(255)),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
    schema="sample_schema"
)

async def create_tables() -> None:
    '''
    Creates all tables
    '''
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

app = FastAPI(title = "Demo FastAPI app running on postgresql")

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
    await create_tables()

@app.on_event("shutdown")
async def shutdown() -> None:
    '''
    Shutdown the app by closing the database connection
    '''
    await database.disconnect()

@database.transaction()
@app.post(
    "/notes/",
    response_model = PutNote,
    status_code = status.HTTP_201_CREATED)
async def create_note(note: PutNote) -> dict:
    '''
    Create a note
    '''
    query = notes.insert().values(text=note.text, completed = note.completed)
    note_id = await database.execute(query)
    print(note_id)
    return {**note.dict(), "id": note_id}

@app.put(
    "/notes/{note_id}",
    response_model = PutNote,
    status_code = status.HTTP_200_OK)
def update_note(note_id: int, note: PutNote) -> dict:
    '''
    Update a note
    '''
    query = notes.update().where(
        notes.c.id == note_id).values(
            text=note.text,
            completed = note.completed)
    database.execute(query)
    return {**note.dict(), "id": note_id}

@database.transaction()
@app.get(
    "/notes/",
    response_model = List[GetNote],
    status_code = status.HTTP_200_OK
    )
async def get_notes(skip: int=0, limit: int = 20) -> list:
    '''
    Get all notes
    '''
    query = notes.select().offset(skip).limit(limit)
    response = await database.fetch_all(query)
    response = [ dict(i.items()) for i in response ]
    print(response)
    return response

@database.transaction()
@app.get(
    "/notes/{note_id}",
    response_model = GetNote,
    status_code = status.HTTP_200_OK
    )
def get_note(note_id: int) -> GetNote:
    '''
    Get a note
    '''
    query = notes.select().where(notes.c.id == note_id)
    return database.fetch_one(query)

@database.transaction()
@app.delete(
    "/notes/{note_id}",
    status_code = status.HTTP_200_OK
    )
def delete_note(note_id: int) -> dict:
    '''
    Deletes given note
    '''
    query = notes.delete().where(notes.c.id == note_id)
    database.execute(query)
    return {'message': f'Message with id {note_id} deleted'}
