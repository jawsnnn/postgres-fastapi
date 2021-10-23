from pydantic import BaseModel

class PutNote(BaseModel):
    text : str
    completed : bool

class GetNote(BaseModel):
    id : int
    text : str
    completed : bool