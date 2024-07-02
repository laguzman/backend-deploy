from fastapi import APIRouter, Depends
from models.note import NoteCreate
from services.note_service import NoteService

router = APIRouter()

def get_note_service():
    return NoteService()

@router.get("/")
async def get_note(service: NoteService = Depends(get_note_service)):
    return await service.get_all_notes()

@router.post("/")
async def create_note(note: NoteCreate, service: NoteService = Depends(get_note_service)):
    return await service.create_note(note)

@router.put("/{id}")
async def update_note(id: str, note: NoteCreate, service: NoteService = Depends(get_note_service)):
    return await service.update_note(id, note)

@router.delete("/{id}")
async def delete_note(id: str, service: NoteService = Depends(get_note_service)):
    return await service.delete_note(id)