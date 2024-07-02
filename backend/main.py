from fastapi import FastAPI
from pydantic import BaseModel
from prisma import Prisma
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteCreate(BaseModel):
    body: str
    archived: bool
    tag: str

class NoteRead(BaseModel):
    id: str
    email: str
    name: str


@app.get("/")
async def get_note():
    async with Prisma() as db:
        data = await db.note.find_many()
    return data


@app.post("/")
async def create_note(note: NoteCreate):
    async with Prisma() as db:
        data = await db.note.create(
            data=note.model_dump()
        )
    return data


@app.put("/{id}")
async def update_note(id: str, note: NoteCreate):
    async with Prisma() as db:
        data = await db.note.update(
            where={"id": id},
            data=note.model_dump()
        )
    return data


@app.delete("/{id}")
async def update_note(id: str,):
    async with Prisma() as db:
        data = await db.note.delete(
            where={"id": id}
        )
    return data
