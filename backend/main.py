import os
from fastapi import FastAPI
from prisma import Prisma

app = FastAPI()
prisma = Prisma()

@app.on_event("startup")
async def startup():
    try:
        await prisma.connect()
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir()}")
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
        # Replace this with an actual query to your database
        result = await prisma.your_model.find_first()
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}