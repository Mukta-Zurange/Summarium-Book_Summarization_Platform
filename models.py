from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

# ---------------- USERS ----------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(10), default="user")
    security_question = Column(String(255), nullable=True)
    security_answer = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="user")

# ---------------- BOOKS ----------------
class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    uploaded_by = Column(Integer, ForeignKey("users.user_id"))
    upload_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="books")
    raw_text = relationship("RawText", back_populates="book", uselist=False)
    summaries = relationship("Summary", back_populates="book")
    chunk_summaries = relationship("ChunkSummary", back_populates="book")

# ---------------- RAW TEXT ----------------
class RawText(Base):
    __tablename__ = "raw_text"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    full_text = Column(Text)

    book = relationship("Book", back_populates="raw_text")

# ---------------- PASTED TEXT ----------------
class PastedText(Base):
    __tablename__ = "pasted_texts"

    pasted_id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    summaries = relationship("Summary", back_populates="pasted_text")
    chunk_summaries = relationship("ChunkSummary", back_populates="pasted_text")

# ---------------- SUMMARIES ----------------

class ChunkSummary(Base):
    __tablename__ = "chunk_summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=True)
    pasted_id = Column(Integer, ForeignKey("pasted_texts.pasted_id"), nullable=True)
    chunk_index = Column(Integer, nullable=False)
    chunk_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="chunk_summaries")
    pasted_text = relationship("PastedText", back_populates="chunk_summaries")

class Summary(Base):
    __tablename__ = "summaries"

    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=True)
    pasted_id = Column(Integer, ForeignKey("pasted_texts.pasted_id"), nullable=True)
    summary_text = Column(Text, nullable=True)
    summary_type = Column(String(50), nullable=True)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="summaries")
    pasted_text = relationship("PastedText", back_populates="summaries")
