from app import routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.auth.router, tags=['Auth'])
app.include_router(routes.notes.router, tags=['Notes'], prefix='/notes')

@app.get('/')
def root():
    return {'message': 'OK'}