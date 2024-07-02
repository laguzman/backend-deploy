from fastapi import FastAPI, Depends
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

# Create a single Prisma instance
db = Prisma()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Dependency to get the database instance
async def get_db():
    return db

@app.get("/")
async def get_note(db: Prisma = Depends(get_db)):
    data = await db.note.find_many()
    return data

@app.post("/")
async def create_note(note: NoteCreate, db: Prisma = Depends(get_db)):
    data = await db.note.create(
        data=note.model_dump()
    )
    return data

@app.put("/{id}")
async def update_note(id: str, note: NoteCreate, db: Prisma = Depends(get_db)):
    data = await db.note.update(
        where={"id": id},
        data=note.model_dump()
    )
    return data

@app.delete("/{id}")
async def delete_note(id: str, db: Prisma = Depends(get_db)):
    data = await db.note.delete(
        where={"id": id}
    )
    return data