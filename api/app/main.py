import json
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routes import users, documents, conversations, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(conversations.router)

# Add before defining routes, after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def main():
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps(dict(msg="App Socrates RAG API Interface")),
        media_type="application/json",
    )


