import typer
from faker import Faker
from sqlalchemy.orm import Session
import random
from datetime import datetime, timezone

from app.db.database import SessionLocal, engine, Base
from app.schemas.user import UserCreate
from app.db.models import User, Document, DocumentChunk, Conversation, Message

# Initialize Typer app
app = typer.Typer()
fake = Faker()
DEFAULT_PASSWD = "0e542d2231"

# Ensure tables are created (using the imported Base and engine)
# Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.command()
def create_superuser(
    name: str = "admin",
    email: str = "admin@admin.com",
    password: str = DEFAULT_PASSWD,
    db_session=None,
):
    """Create an admin user"""
    db = SessionLocal() if not db_session else db_session
    users = [UserCreate(name=name, email=email, password=password),]
    instance = User.create_users(db, users)
    typer.echo(f"Superuser {email} created!")


@app.command()
def load_users(
    count: int = typer.Option(
        10, "--count", "-c", help="Number of fake users to create."
    )
):
    """Loads fake user data into the database."""
    db: Session = next(get_db())
    typer.echo(f"Creating {count} fake users...")
    user_list = [
        UserCreate(
            name=fake.name(),
            email=fake.email(),
            password=DEFAULT_PASSWD,
        )
        for _ in range(count)
    ]
    user_instances = User.create_users(db=db, users=user_list)
    typer.echo(f"Successfully created {len(user_instances)} users.")


@app.command()
def load_documents(
    count: int = typer.Option(
        50, "--count", "-c", help="Number of fake documents to create."
    )
):
    """Loads fake document data into the database."""
    db: Session = next(get_db())
    users = db.query(User).all()
    if not users:
        typer.echo("No users found. Please run 'load-users' first.")
        return

    typer.echo(f"Creating {count} fake documents...")
    for _ in range(count):
        document = Document(
            filename=fake.file_name(category="text"),
            file_type=random.choice(["txt", "pdf", "docx"]),
            file_size=fake.random_int(min=1000, max=1000000),
            uploaded_at=fake.date_time_this_year(tzinfo=timezone.utc),
            user_id=random.choice(users).id if users else None,
        )
        db.add(document)
    db.commit()
    typer.echo(f"Successfully created {count} documents.")


@app.command()
def load_conversations_messages(
    conversations_count: int = typer.Option(
        20,
        "--conversations-count",
        "-c",
        help="Number of fake conversations to create.",
    ),
    messages_per_conversation: int = typer.Option(
        5,
        "--messages-per_conversation",
        "-m",
        help="Number of fake messages per conversation.",
    ),
):
    """Loads fake conversation and message data into the database."""
    db: Session = next(get_db())
    documents = db.query(Document).all()
    if not documents:
        typer.echo("No documents found. Please run 'load-documents' first.")
        return

    typer.echo(
        f"Creating {conversations_count} fake conversations with {
            messages_per_conversation} messages each..."
    )
    for _ in range(conversations_count):
        document = random.choice(documents)
        conversation = Conversation(
            document_id=document.id,
            title=fake.sentence(nb_words=6),
            created_at=fake.date_time_this_year(tzinfo=timezone.utc),
            updated_at=fake.date_time_this_year(tzinfo=timezone.utc),
        )
        db.add(conversation)
        db.flush()  # Flush to get conversation.id before adding messages

        for msg_index in range(messages_per_conversation):
            message_role = "user" if msg_index % 2 == 0 else "assistant"
            message = Message(
                conversation_id=conversation.id,
                role=message_role,
                content=fake.paragraph(nb_sentences=2),
                created_at=fake.date_time_this_year(tzinfo=timezone.utc),
            )
            db.add(message)
    db.commit()
    typer.echo(
        f"Successfully created {
            conversations_count} conversations and their messages."
    )


@app.command()
def load_dev_data():
    """Load fake data for development purposes."""
    load_users(count=10)
    load_documents(count=10)
    load_conversations_messages(
        conversations_count=10,
        messages_per_conversation=4,
    )


if __name__ == "__main__":
    app()
