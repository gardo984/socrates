from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
from sqlalchemy.orm import Session
from typing import List


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False, default="")

    @classmethod
    def get_password_hash(cls, value: str) -> str:
        from app.core.security import hash_password

        return hash_password(value)

    @classmethod
    def create_users(
        cls,
        db: Session,
        users: List,
        # current_user: Optional["UserCreate"] = None,
    ) -> List:
        users_to_create: List[cls] = []
        for user_data in users:
            user_data.password = cls.get_password_hash(user_data.password)
            payload = user_data.model_dump()
            payload.pop("password")
            payload.update({"hashed_password": user_data.password})
            # if current_user:
            #     payload.update({"created_by_id": current_user.id})
            db_user = cls(**payload)
            db.add(db_user)
            users_to_create.append(db_user)

        db.commit()
        for user in users_to_create:
            db.refresh(user)

        if len(users_to_create) > 1:
            return users_to_create
        else:
            return users_to_create[0]


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10))  # "txt", "pdf", "docx"
    file_size = Column(Integer)  # size in bytes
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    user = relationship("User", backref="documents")
    chunks = relationship(
        "DocumentChunk", back_populates="document", cascade="all, delete-orphan"
    )
    conversations = relationship(
        "Conversation", back_populates="document", cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer)  # order of chunk in the document
    content = Column(Text, nullable=False)
    chunk_size = Column(Integer)  # number of characters
    vector_id = Column(String(255))  # ID in vector store (Chroma/other)

    # Relationships
    document = relationship("Document", back_populates="chunks")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    title = Column(String(255), default="New Conversation")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    document = relationship("Document", back_populates="conversations")
    messages = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey(
        "conversations.id"), nullable=False)
    role = Column(String(20))  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    metadata_ = Column(
        "metadata", JSON, nullable=True
    )  # store retrieved chunk references, scores, etc.

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
