from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, select, update, delete
from pydantic import BaseModel
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, index=True)
    archived = Column(Boolean, default=False)
    tag = Column(String)

# Pydantic models
class NoteCreate(BaseModel):
    body: str
    archived: bool
    tag: str

class NoteRead(BaseModel):
    id: int
    body: str
    archived: bool
    tag: str

    class Config:
        orm_mode = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/", response_model=list[NoteRead])
async def get_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NoteModel))
    notes = result.scalars().all()
    return [NoteRead.from_orm(note) for note in notes]

@app.post("/", response_model=NoteRead)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    db_note = NoteModel(**note.dict())
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return NoteRead.from_orm(db_note)

@app.put("/{note_id}", response_model=NoteRead)
async def update_note(note_id: int, note: NoteCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(update(NoteModel).where(NoteModel.id == note_id).values(**note.dict()).returning(NoteModel))
    updated_note = result.scalars().first()
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.commit()
    return NoteRead.from_orm(updated_note)

@app.delete("/{note_id}", response_model=NoteRead)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(NoteModel).where(NoteModel.id == note_id).returning(NoteModel))
    deleted_note = result.scalars().first()
    if deleted_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.commit()
    return NoteRead.from_orm(deleted_note)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)