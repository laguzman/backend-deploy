from repositories.note_repository import NoteRepository
from models.note import NoteCreate

class NoteService:
    def __init__(self):
        self.repository = NoteRepository()

    async def get_all_notes(self):
        return await self.repository.get_all_notes()

    async def create_note(self, note: NoteCreate):
        return await self.repository.create_note(note)

    async def update_note(self, id: str, note: NoteCreate):
        return await self.repository.update_note(id, note)

    async def delete_note(self, id: str):
        return await self.repository.delete_note(id)