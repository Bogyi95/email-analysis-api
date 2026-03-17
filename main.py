from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import EmailRecord

app = FastAPI()
Base.metadata.create_all(bind=engine)

class Email(BaseModel):
    subject: str
    body: str

@app.get("/")
def root():
    return {"message": "Email Analysis API is running"}

def classify_email(text: str):
    text = text.lower()

    if "invoice" in text or "payment" in text:
        return "finance"
    if "meeting" in text or "schedule" in text:
        return "work"
    if "offer" in text or "discount" in text:
        return "marketing"
    return "general"

def detect_priority(text: str):
    text = text.lower()

    if "urgent" in text or "asap" in text or "immediately" in text or "important" in text:
        return "high"
    return "normal"

def summarize(text: str):
    sentences = text.split(".")
    return sentences[0]

@app.post("/analyze-email")
def analyze_email(email: Email):

    db = SessionLocal()

    category = classify_email(email.body)
    priority = detect_priority(email.body)
    summary = summarize(email.body)

    record = EmailRecord(
        subject = email.subject,
        body = email.body,
        category = category,
        priority = priority,
        summary = summary
    )

    db.add(record)
    db.commit()

    return{
        "category": category,
        "priority": priority,
        "summary": summary
    }

@app.get("/emails")
def get_emails():
    db = SessionLocal()
    emails = db.query(EmailRecord).all()
    return emails