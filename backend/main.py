import os
import sys
from fastapi import FastAPI
from prisma import Prisma

app = FastAPI()
prisma = Prisma()

@app.on_event("startup")
async def startup():
    try:
        print(f"Python version: {sys.version}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir()}")
        print(f"Prisma binary path: {Prisma.binary_path}")
        print(f"Contents of Prisma binary directory: {os.listdir(os.path.dirname(Prisma.binary_path))}")
        await prisma.connect()
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        print(f"Prisma version: {prisma.__version__}")
        raise

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test-db")
async def test_db():
    try:
        # Replace 'Note' with your actual model name
        result = await prisma.note.find_first()
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}