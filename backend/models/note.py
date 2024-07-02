from pydantic import BaseModel

class NoteCreate(BaseModel):
    body: str
    archived: bool
    tag: str

class NoteRead(BaseModel):
    id: str
    email: str
    name: str