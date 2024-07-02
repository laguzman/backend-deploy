from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.note_controller import router as note_router
from prisma import Prisma

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note_router)

prisma = Prisma()


@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()