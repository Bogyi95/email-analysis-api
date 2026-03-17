from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import EmailRecord
from nlp_model import classify_email_ml
from email_fetcher import fetch_emails
import os
from dotenv import load_dotenv

load_dotenv() 

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

    category = classify_email_ml(email.body)
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

@app.post("/scan-inbox")
def scan_inbox():
    username = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    emails = fetch_emails(username, password, limit=10)
    results = []

    for email_data in emails:
        category = classify_email_ml(email_data["body"])
        priority = detect_priority(email_data["body"])
        summary = summarize(email_data["body"])

        db = SessionLocal()

        record = EmailRecord(
            subject = email_data["subject"],
            body = email_data["body"],
            category = category,
            priority = priority,
            summary = summary
        )
        
        db.add(record)
        db.commit()

        results.append({
            "subject": email_data["subject"],
            "category": category,
            "priority": priority
        })

    return {"processed_emails": results}