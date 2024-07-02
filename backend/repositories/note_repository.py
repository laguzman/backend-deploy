from prisma import Prisma
from models.note import NoteCreate

class NoteRepository:
    async def get_all_notes(self):
        async with Prisma() as db:
            return await db.note.find_many()

    async def create_note(self, note: NoteCreate):
        async with Prisma() as db:
            return await db.note.create(data=note.model_dump())

    async def update_note(self, id: str, note: NoteCreate):
        async with Prisma() as db:
            return await db.note.update(where={"id": id}, data=note.model_dump())

    async def delete_note(self, id: str):
        async with Prisma() as db:
            return await db.note.delete(where={"id": id})