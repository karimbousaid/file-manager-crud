from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .endpoints import users, files 

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# custom api info
app = FastAPI(
    title="File Manager API",
    description="API for managing user authentication and file CRUD operations",
    version="1.0.0"
)

# allow frontend access
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)  # Authentication routes
app.include_router(files.router)  # File Manager CRUD routes