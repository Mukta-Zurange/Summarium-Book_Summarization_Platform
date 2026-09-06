# =========================
# IMPORTS
# =========================
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import BackgroundTasks
from database import SessionLocal
from fastapi import Request
from sqlalchemy import func
from models import Base, User, Book, RawText, Summary, PastedText, ChunkSummary, PasswordReset, ChatMessage
import shutil
import os
import os
from dotenv import load_dotenv


from database import SessionLocal, engine
from models import Base, User, Book, RawText, Summary
from auth_utils import hash_password, verify_password
from summarizer import summarize_text

# =========================
# DATABASE INIT
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# APP INIT
# =========================
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =========================
# CONFIG
# =========================
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# JWT FUNCTIONS
# =========================
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


# ADD THIS RIGHT AFTER get_current_user:
def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
    #if current_user.role != "admin":
        #raise HTTPException(status_code=403, detail="Admin access required")
    #return current_user


# =========================
# SCHEMAS
# =========================
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    security_question: str = None
    security_answer: str = None


def run_summary_in_background(book_id: int, db: Session):
    try:
        raw_text = db.query(RawText).filter(RawText.book_id == book_id).first()
        if not raw_text:
            return
        final_summary = summarize_text(raw_text.full_text)
        new_summary = Summary(
            book_id=book_id,
            summary_text=final_summary,
            summary_type="short"
        )
        db.add(new_summary)
        db.commit()
    finally:
        db.close()

# =========================
# ROUTES
# =========================

@app.get("/")
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/app")
def main_app(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin")
def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/verify-token")
def verify_token(current_user: User = Depends(get_current_user)):
    return {"valid": True}

# ---------- REGISTER ----------
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"message": "Email already registered"}

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        security_question=user.security_question,
        security_answer=user.security_answer.lower().strip() if user.security_answer else None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# ---------- LOGIN ----------
@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == username).first()

    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(db_user.user_id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role  # FIXED: was user.role
    }


# ---------- GET SECURITY QUESTION ----------
@app.post("/get-security-question")
def get_security_question(email: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.security_question:
        raise HTTPException(status_code=404, detail="No security question found for this email")
    return {"question": user.security_question}


# ---------- RESET PASSWORD ----------
@app.post("/reset-password")
def reset_password(
    email: str = Form(...),
    answer: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.security_answer.lower().strip() != answer.lower().strip():
        raise HTTPException(status_code=400, detail="Incorrect answer")

    user.password = hash_password(new_password)
    db.commit()

    return {"message": "Password reset successfully"}


# ---------- SET SECURITY QUESTION (after register) ----------
@app.post("/set-security-question")
def set_security_question(
    question: str = Form(...),
    answer: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.security_question = question
    current_user.security_answer = answer.lower().strip()
    db.commit()
    return {"message": "Security question set successfully"}


# ---------- UPLOAD BOOK ----------

@app.post("/upload-book")
def upload_book(
    title: str,
    author: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Book).filter(
        func.lower(Book.title) == func.lower(title),
        func.lower(Book.author) == func.lower(author)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"This book already exists in the database with Book ID: {existing.book_id}. Check in Uploaded Books."
        )

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    from extractor import extract_text
    extracted_text = extract_text(file_path)

    new_book = Book(
        title=title,
        author=author,
        uploaded_by=current_user.user_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    raw_text = RawText(
        book_id=new_book.book_id,
        full_text=extracted_text
    )
    db.add(raw_text)
    db.commit()

    return {
        "message": "Book uploaded successfully",
        "book_id": new_book.book_id
    }


@app.post("/upload-pasted-text")
def upload_pasted_text(
    text: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_entry = PastedText(
        content=text,
        uploaded_by=current_user.user_id
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {
        "message": "Text uploaded successfully",
        "pasted_id": f"T{new_entry.pasted_id}"
    }

@app.post("/upload-youtube")
def upload_youtube(
    url: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    import re

    # Extract video ID from URL
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if not video_id_match:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    video_id = video_id_match.group(1)

    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id)
        text = " ".join([entry.text for entry in fetched])
    except TranscriptsDisabled:
        raise HTTPException(status_code=400, detail="This video has captions disabled")
    except NoTranscriptFound:
        raise HTTPException(status_code=400, detail="No transcript found for this video")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch transcript: {str(e)}")

    if len(text.strip()) < 100:
        raise HTTPException(status_code=400, detail="Transcript too short to summarize")

    new_entry = PastedText(
        content=text,
        uploaded_by=current_user.user_id
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message": "YouTube transcript extracted successfully",
        "pasted_id": f"T{new_entry.pasted_id}",
        "word_count": len(text.split())
    }

# ---------- GENERATE SUMMARY ----------
@app.post("/generate-summary/{item_id}")
def generate_summary(
    item_id: str,
    background_tasks: BackgroundTasks,
    format: str = "paragraph",
    length: str = "medium",
    force: bool = False,
    role: str = "general",
    db: Session = Depends(get_db)
):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        entry = db.query(PastedText).filter(PastedText.pasted_id == pasted_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Pasted text not found")
        text = entry.content
        book_id = None
        pasted_ref = pasted_id
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        book = db.query(Book).filter(Book.book_id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        raw = db.query(RawText).filter(RawText.book_id == book_id).first()
        if not raw:
            raise HTTPException(status_code=404, detail="No text found for this book")
        text = raw.full_text
        pasted_ref = None

    summary_type = f"{format}_{length}_{role}"

    # Check cache only if force=False
    if not force:
        if book_id:
            cached = db.query(Summary).filter(
                Summary.book_id == book_id,
                Summary.summary_type == summary_type,
                Summary.summary_text != "processing",
                Summary.summary_text != None
            ).order_by(Summary.summary_id.desc()).first()
        else:
            cached = db.query(Summary).filter(
                Summary.pasted_id == pasted_ref,
                Summary.summary_type == summary_type,
                Summary.summary_text != "processing",
                Summary.summary_text != None
            ).order_by(Summary.summary_id.desc()).first()

        if cached:
            return {
                "status": "done",
                "summary": cached.summary_text,
                "cached": True
            }

    new_summary = Summary(
        book_id=book_id,
        pasted_id=pasted_ref,
        summary_text="processing",
        summary_type=summary_type,
        progress=0
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    summary_id = new_summary.summary_id

    def run_summary(summary_id, text, format, length, book_id, pasted_ref, role="general"):
        from database import SessionLocal
        db2 = SessionLocal()
        try:
            if book_id:
                existing = db2.query(ChunkSummary).filter(
                    ChunkSummary.book_id == book_id
                ).order_by(ChunkSummary.chunk_index).all()
            else:
                existing = db2.query(ChunkSummary).filter(
                    ChunkSummary.pasted_id == pasted_ref
                ).order_by(ChunkSummary.chunk_index).all()

            if existing:
                print(f"Reusing {len(existing)} saved chunk summaries")
                existing_chunks = [c.chunk_summary for c in existing]
                result, _ = summarize_text(text, format=format, length=length, existing_chunks=existing_chunks, role=role)
            else:
                result, chunk_summaries = summarize_text(text, format=format, length=length, role=role)
                for i, cs in enumerate(chunk_summaries):
                    db2.add(ChunkSummary(
                        book_id=book_id,
                        pasted_id=pasted_ref,
                        chunk_index=i,
                        chunk_summary=cs
                    ))
                db2.commit()

            record = db2.query(Summary).filter(Summary.summary_id == summary_id).first()
            if record:
                record.summary_text = result
                record.progress = 100
                db2.commit()
        finally:
            db2.close()

    background_tasks.add_task(run_summary, summary_id, text, format, length, book_id, pasted_ref, role)
    return {"status": "processing", "summary_id": summary_id}


# ---------- PROFILE ----------
@app.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email
    }


# ---------- SUMMARY STATUS ----------
@app.get("/summary-status/{item_id}")
def summary_status(item_id: str, db: Session = Depends(get_db)):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        summary = db.query(Summary).filter(
            Summary.pasted_id == pasted_id
        ).order_by(Summary.summary_id.desc()).first()
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        summary = db.query(Summary).filter(
            Summary.book_id == book_id
        ).order_by(Summary.summary_id.desc()).first()

    if not summary:
        return {"status": "not_found"}
    if summary.summary_text == "processing":
        return {"status": "processing", "progress": summary.progress or 0}
    return {"status": "done", "summary": summary.summary_text, "progress": 100}


# ---------- SUMMARY HISTORY ----------
@app.get("/summary-history/{item_id}")
def summary_history(item_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        summaries = db.query(Summary).filter(
            Summary.pasted_id == pasted_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).all()
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        summaries = db.query(Summary).filter(
            Summary.book_id == book_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).all()

    if not summaries:
        raise HTTPException(status_code=404, detail="No summaries found")

    return [
        {
            "summary_id": s.summary_id,
            "summary_text": s.summary_text,
            "summary_type": s.summary_type or "unknown",
            "version": i + 1
        }
        for i, s in enumerate(summaries)
    ]

# ---------- ALL BOOKS ----------
@app.get("/my-books")
def get_all_books(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author
        }
        for book in books
    ]


@app.get("/quiz/{item_id}")
def get_quiz(item_id: str, db: Session = Depends(get_db)):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        summary = db.query(Summary).filter(
            Summary.pasted_id == pasted_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        summary = db.query(Summary).filter(
            Summary.book_id == book_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()

    if not summary:
        raise HTTPException(status_code=404, detail="No summary found. Generate a summary first.")

    from summarizer import generate_quiz
    try:
        quiz = generate_quiz(summary.summary_text)
        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {str(e)}")



# ---------- MIND MAP ----------
@app.get("/mindmap/{item_id}")
def get_mindmap(item_id: str, db: Session = Depends(get_db)):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        summary = db.query(Summary).filter(
            Summary.pasted_id == pasted_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        summary = db.query(Summary).filter(
            Summary.book_id == book_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()

    if not summary:
        raise HTTPException(status_code=404, detail="No summary found. Generate a summary first.")

    from summarizer import generate_mindmap_data
    mindmap = generate_mindmap_data(summary.summary_text)
    return {"mindmap": mindmap}


# ---------- ASK AI ----------
@app.post("/ask/{item_id}")
def ask_ai(
    item_id: str,
    question: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        entry = db.query(PastedText).filter(PastedText.pasted_id == pasted_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Pasted text not found")
        text = entry.content
        book_id = None
        pasted_ref = pasted_id
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        raw = db.query(RawText).filter(RawText.book_id == book_id).first()
        if not raw:
            raise HTTPException(status_code=404, detail="No text found for this book")
        text = raw.full_text
        pasted_ref = None

    if book_id:
        history = db.query(ChatMessage).filter(
            ChatMessage.book_id == book_id
        ).order_by(ChatMessage.id.desc()).limit(6).all()
    else:
        history = db.query(ChatMessage).filter(
            ChatMessage.pasted_id == pasted_ref
        ).order_by(ChatMessage.id.desc()).limit(6).all()

    history = list(reversed(history))
    context = text[:6000] if len(text) > 6000 else text

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers questions based ONLY on the document provided. "
                "If the answer is not in the document, say 'I could not find that in the document.' "
                "Be concise and accurate.\n\n"
                f"Document:\n{context}"
            )
        }
    ]

    for msg in history:
        messages.append({"role": msg.role, "content": msg.message})

    messages.append({"role": "user", "content": question})

    from summarizer import groq_client
    import time
    while True:
        try:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages
            )
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                time.sleep(10)
            else:
                raise HTTPException(status_code=500, detail=str(e))

    answer = response.choices[0].message.content

    db.add(ChatMessage(book_id=book_id, pasted_id=pasted_ref, role="user", message=question))
    db.add(ChatMessage(book_id=book_id, pasted_id=pasted_ref, role="assistant", message=answer))
    db.commit()

    return {"answer": answer}


@app.get("/chat-history/{item_id}")
def get_chat_history(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        messages = db.query(ChatMessage).filter(
            ChatMessage.pasted_id == pasted_id
        ).order_by(ChatMessage.id.asc()).all()
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        messages = db.query(ChatMessage).filter(
            ChatMessage.book_id == book_id
        ).order_by(ChatMessage.id.asc()).all()

    return [
        {"role": msg.role, "message": msg.message}
        for msg in messages
    ]

@app.get("/chat-suggestions/{item_id}")
def get_chat_suggestions(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        entry = db.query(PastedText).filter(PastedText.pasted_id == pasted_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Text not found")
        text = entry.content
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        raw = db.query(RawText).filter(RawText.book_id == book_id).first()
        if not raw:
            raise HTTPException(status_code=404, detail="Book not found")
        text = raw.full_text

    context = text[:3000] if len(text) > 3000 else text

    from summarizer import groq_client
    import time
    while True:
        try:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{
                    "role": "user",
                    "content": (
                        "Based on the following document, generate exactly 4 short interesting questions "
                        "a reader might want to ask about it. "
                        "Return ONLY a JSON array of 4 strings, no explanation, no markdown, no backticks.\n"
                        'Example: ["What is the main topic?", "Who are the key people mentioned?", "What are the main conclusions?", "What methods were used?"]\n\n'
                        f"Document:\n{context}"
                    )
                }]
            )
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                time.sleep(10)
            else:
                raise HTTPException(status_code=500, detail=str(e))

    import json
    raw = response.choices[0].message.content.strip()
    raw = raw.strip("```json").strip("```").strip()
    try:
        suggestions = json.loads(raw)
        if not isinstance(suggestions, list):
            suggestions = []
    except:
        suggestions = []

    return {"suggestions": suggestions[:4]}


@app.post("/explain")
def explain_text(
    sentence: str = Form(...),
    mode: str = Form(default="explain"),
    current_user: User = Depends(get_current_user)
):
    mode_prompts = {
        "explain": "Explain the following sentence clearly and accurately in 2-3 sentences:",
        "simplify": "Rewrite the following sentence in very simple plain language, no jargon:",
        "example": "Give a concrete real-world example that illustrates the following sentence:",
        "eli5": "Explain the following sentence like I am 10 years old, using very simple words:"
    }

    prompt = mode_prompts.get(mode, mode_prompts["explain"])

    from summarizer import groq_client
    import time
    while True:
        try:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{
                    "role": "user",
                    "content": f"{prompt}\n\n\"{sentence}\""
                }]
            )
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                time.sleep(10)
            else:
                raise HTTPException(status_code=500, detail=str(e))

    return {"result": response.choices[0].message.content.strip()}


# ---------- ADMIN ROUTES ----------
@app.get("/admin/stats")
def admin_stats(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_books = db.query(Book).count()
    total_summaries = db.query(Summary).filter(Summary.summary_text != "processing").count()
    return {
        "total_users": total_users,
        "total_books": total_books,
        "total_summaries": total_summaries
    }

@app.get("/admin/users")
def admin_get_users(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "user_id": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        }
        for u in users
    ]

@app.delete("/admin/users/{user_id}")
def admin_delete_user(user_id: int, current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete admin user")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@app.get("/admin/books")
def admin_get_books(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "book_id": b.book_id,
            "title": b.title,
            "author": b.author,
            "uploaded_by": b.uploaded_by
        }
        for b in books
    ]

@app.delete("/admin/books/{book_id}")
def admin_delete_book(book_id: int, current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}

@app.get("/admin/book-stats")
def admin_book_stats(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    books = db.query(Book).all()
    result = []
    for book in books:
        summaries = db.query(Summary).filter(
            Summary.book_id == book.book_id,
            Summary.summary_text != "processing"
        ).all()
        result.append({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "total_summaries": len(summaries),
            "types": list(set([s.summary_type for s in summaries if s.summary_type]))
        })
    return result


@app.get("/insights/{item_id}")
def get_insights(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if item_id.upper().startswith("T"):
        pasted_id = int(item_id[1:])
        summary = db.query(Summary).filter(
            Summary.pasted_id == pasted_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()
    else:
        book_id = int(item_id[1:]) if item_id.upper().startswith("B") else int(item_id)
        summary = db.query(Summary).filter(
            Summary.book_id == book_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()

    if not summary:
        raise HTTPException(status_code=404, detail="No summary found. Generate a summary first.")

    from summarizer import groq_client
    import time, json

    while True:
        try:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{
                    "role": "user",
                    "content": (
                        "Extract exactly 5 key insights from the following summary. "
                        "Each insight must be a single concise sentence — the most important takeaway. "
                        "Return ONLY a JSON array of 5 strings, no explanation, no markdown, no backticks.\n"
                        'Example: ["Insight one.", "Insight two.", "Insight three.", "Insight four.", "Insight five."]\n\n'
                        f"Summary:\n{summary.summary_text}"
                    )
                }]
            )
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                time.sleep(10)
            else:
                raise HTTPException(status_code=500, detail=str(e))

    raw = response.choices[0].message.content.strip()
    raw = raw.strip("```json").strip("```").strip()

    try:
        insights = json.loads(raw)
        if not isinstance(insights, list):
            insights = []
    except:
        insights = []

    return {"insights": insights[:5]}


@app.get("/user-history")
def get_user_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get all books uploaded by user with their latest summary
    books = db.query(Book).filter(Book.uploaded_by == current_user.user_id).all()
    
    result = []
    for book in books:
        latest_summary = db.query(Summary).filter(
            Summary.book_id == book.book_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()
        
        if latest_summary:
            result.append({
                "id": f"B{book.book_id}",
                "title": book.title,
                "author": book.author,
                "summary_type": latest_summary.summary_type or "general",
                "created_at": latest_summary.created_at.strftime("%b %d, %Y") if latest_summary.created_at else ""
            })
    
    # Also get pasted texts
    pasted = db.query(PastedText).filter(PastedText.uploaded_by == current_user.user_id).all()
    for entry in pasted:
        latest_summary = db.query(Summary).filter(
            Summary.pasted_id == entry.pasted_id,
            Summary.summary_text != "processing"
        ).order_by(Summary.summary_id.desc()).first()
        
        if latest_summary:
            preview = entry.content[:40].strip() + "..." if len(entry.content) > 40 else entry.content
            result.append({
                "id": f"T{entry.pasted_id}",
                "title": preview,
                "author": "Pasted Text",
                "summary_type": latest_summary.summary_type or "general",
                "created_at": latest_summary.created_at.strftime("%b %d, %Y") if latest_summary.created_at else ""
            })
    
    # Sort by most recent first
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return result