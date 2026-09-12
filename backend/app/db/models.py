from datetime import datetime,timezone
from sqlalchemy import DateTime , String, ForeignKey, UniqueConstraint, ForeignKeyConstraint, PrimaryKeyConstraint, Text, Enum
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    email_domain: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc),nullable = False)

#defining Role table
class Role(Base):
    __tablename__ = "roles"

    id : Mapped[int]= mapped_column(primary_key=True)
    org_id : Mapped[int]=mapped_column(
        ForeignKey("organizations.id",ondelete = "CASCADE"),
        nullable = False,
    )
    role_name : Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
    __table_args__ = (
        UniqueConstraint("id","org_id"),
        UniqueConstraint("org_id","role_name")
    )


#user Table 
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    org_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint("id", "org_id"),
        UniqueConstraint("org_id", "email"),
        ForeignKeyConstraint(
            ["role_id","org_id"],
            ["roles.id","roles.org_id"],
            ondelete = "RESTRICT",
        ),
    )


#documents 
class Document(Base):
    __tablename__ = "documents"
    id : Mapped[int] = mapped_column(primary_key = True)
    org_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id",ondelete="CASCADE"),
        nullable = False,
    )
    filename: Mapped[str]=mapped_column(
        String(255),
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    file_type: Mapped[str]=mapped_column(
        String(100),
        nullable=False,
    )
    file_size: Mapped[int]=mapped_column(
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint("id", "org_id"),
    )

#docmument permission
class DocumentPermission(Base):
    __tablename__ = "document_permissions"
    doc_id : Mapped[int]=mapped_column(
        nullable=False,
    )
    role_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    org_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    __table_args__ = (
        PrimaryKeyConstraint("doc_id","role_id"),
        ForeignKeyConstraint(
            ["doc_id", "org_id"],
            ["documents.id", "documents.org_id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["role_id", "org_id"],
            ["roles.id", "roles.org_id"],
            ondelete="CASCADE",
        ),
    )

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id : Mapped[int]=mapped_column(
        primary_key=True,
    )
    doc_id : Mapped[int]=mapped_column(
        ForeignKey('documents.id',ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index:Mapped[int]=mapped_column(
        nullable=False,
    )
    chunk_text:Mapped[str]=mapped_column(
        Text,
        nullable=False,
    )
    embedding:Mapped[list[float]]=mapped_column(
        Vector(384),
        nullable=False,
    )
    chunk_metadata :Mapped[dict]=mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
    )
    __table_args__=(
        UniqueConstraint("doc_id","chunk_index"),
    )
#conversation for every user
class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    org_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "org_id"],
            ["users.id", "users.org_id"],
            ondelete="CASCADE",
        ),
    )

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    role: Mapped[str] = mapped_column(
        Enum(
            "user",
            "assistant",
            "system",
            name="message_role",
        ),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )