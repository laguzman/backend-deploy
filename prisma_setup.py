import os
from prisma import Prisma

def setup_prisma():
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir()}")
    print(f"Prisma binary path: {Prisma.binary_path}")
    prisma = Prisma()
    print("Prisma instance created")

if __name__ == "__main__":
    setup_prisma()