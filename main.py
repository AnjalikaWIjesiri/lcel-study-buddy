

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = FastAPI(title="Smart Study Buddy API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Gemini LLM ───────────────────────────────────────────────
def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not set in .env")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key
    )

parser = StrOutputParser()

# ── Request models ───────────────────────────────────────────
class NotesRequest(BaseModel):
    notes: str

class QuizAnswerRequest(BaseModel):
    quiz: str
    student_answers: str

# ── LCEL Chains ──────────────────────────────────────────────
def make_analyzer_chain(llm):
    prompt = ChatPromptTemplate.from_template("""
You are a smart study analyzer.

Read these student notes carefully:
{notes}

Find the TOP 3 topics the student might struggle with.
Format exactly like this:
1. [Topic Name] - [Why it's hard]
2. [Topic Name] - [Why it's hard]
3. [Topic Name] - [Why it's hard]
""")
    return prompt | llm | parser


def make_quiz_chain(llm):
    prompt = ChatPromptTemplate.from_template("""
You are a quiz maker for students.

Weak topics: {weak_topics}

Create exactly 3 multiple choice questions, one per topic.

Use this EXACT format for each question (very important!):

Question 1: [question text here]
A) [option text]
B) [option text]
C) [option text]
D) [option text]
Correct Answer: [letter only, e.g. B]

Question 2: [question text here]
A) [option text]
B) [option text]
C) [option text]
D) [option text]
Correct Answer: [letter only]

Question 3: [question text here]
A) [option text]
B) [option text]
C) [option text]
D) [option text]
Correct Answer: [letter only]

Keep questions clear and educational. You can add emojis to question text but NOT to the options or correct answer line.
""")
    return prompt | llm | parser


def make_tips_chain(llm):
    prompt = ChatPromptTemplate.from_template("""
You are a friendly study coach.

Student weak topics: {weak_topics}

Give:
1. 3 practical study tips specific to these topics
2. One motivational message at the end

Be friendly and use emojis! 🎯
""")
    return prompt | llm | parser


def make_checker_chain(llm):
    prompt = ChatPromptTemplate.from_template("""
You are a kind teacher checking answers.

Quiz: {quiz}
Student answers: {student_answers}

For each question say CORRECT or WRONG, explain if wrong.
Give a final score. Be encouraging!
""")
    return prompt | llm | parser


# ── Endpoints ────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Smart Study Buddy API is running!"}


@app.post("/analyze")
def analyze_notes(request: NotesRequest):
    """Find weak topics from notes"""
    try:
        llm = get_llm()
        result = make_analyzer_chain(llm).invoke({"notes": request.notes})
        return {"weak_topics": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/quiz")
def generate_quiz(request: NotesRequest):
    """Analyze notes → generate quiz (two chained steps)"""
    try:
        llm = get_llm()
        # find weak topics
        weak_topics = make_analyzer_chain(llm).invoke({"notes": request.notes})
        # build quiz from those topics
        quiz = make_quiz_chain(llm).invoke({"weak_topics": weak_topics})
        return {"weak_topics": weak_topics, "quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tips")
def generate_tips(request: NotesRequest):
    """Analyze notes → generate study tips (two chained steps)"""
    try:
        llm = get_llm()
        weak_topics = make_analyzer_chain(llm).invoke({"notes": request.notes})
        tips = make_tips_chain(llm).invoke({"weak_topics": weak_topics})
        return {"weak_topics": weak_topics, "tips": tips}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check")
def check_answers(request: QuizAnswerRequest):
    """Grade student answers"""
    try:
        llm = get_llm()
        result = make_checker_chain(llm).invoke({
            "quiz": request.quiz,
            "student_answers": request.student_answers
        })
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))