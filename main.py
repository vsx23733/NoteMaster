from fastapi import FastAPI, HTTPException, Depends, Query, Form, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Dict
import os
import json
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from config import QUESTIONS_DIR, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, USER_DB_DIR
from utils.note_manager import load_notes, save_note, delete_note, update_note
from utils.question_generator import generate_questions, evaluate_answer, load_question, update_questions, delete_all_questions
from utils.stats_manager import get_all_stats, save_quiz_result, delete_note_stats, delete_all_stats
from models.models import *
from db.user_db import users_db
from auth import *


app = FastAPI()


@app.post("/auth/login", response_model=Token)
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer", "username": request.username, "email": user["email"]}


@app.post("/auth/signup", response_model=Token)
def signup(request: SignupRequest):

    with open(USER_DB_DIR, "r") as fb:
        users = json.load(fb)
    
    if request.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(request.password)


    users[request.username] = {
                "username": request.username,
                "email": request.email,
                "hashed_password": hashed_password, 

            }

    with open(USER_DB_DIR, "w") as fb:
        json.dump(users, fb, indent=2)

    token = create_access_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer", "username": request.username, "email": request.email}


@app.put("/auth/edit-account", response_model=User)
def edit_account(request: EditAccountRequest):
    username = get_current_user(request.token)
    print(username)
    with open(USER_DB_DIR, "r") as fb:
        users = json.load(fb)

    user = users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.email:
        user["email"] = request.email
    if request.username:
        user["username"] = request.username
    
    users_db[request.username] = user
    return user


@app.delete("/auth/delete-account")
def delete_account(request: DeleteAccountRequest):
    with open(USER_DB_DIR, "r") as fb:
        users = json.load(fb)
        
    username = get_current_user(request.token)
    
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    del users_db[username]
    return {"detail": "Account deleted successfully"}

# ==============================
# 📒 NOTES ENDPOINTS (SECURED)
# ==============================

@app.get("/notes")
def get_notes():
    return load_notes()


@app.post("/notes")
def create_note(title: str, content: str):
    save_note(title, content)
    return {"message": "Note saved successfully"}


@app.put("/notes")
def edit_note(title: str, content: str):
    if update_note(title, content):
        return {"message": "Note updated successfully"}
    raise HTTPException(status_code=400, detail="Error updating note")


@app.delete("/notes")
def remove_note(title: str):
    delete_note(title)
    return {"message": "Note deleted successfully"}

# ==============================
# ❓ QUESTIONS ENDPOINTS
# ==============================


@app.get("/questions")
def get_questions(title: str):
    questions = load_question(title)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions


@app.post("/questions")
def generate_question(request: QuestionRequest):
    return generate_questions(request.note_title, request.note_content)


@app.put("/questions")
def update_question_file(new_questions, note_title):
    update_questions(new_questions, note_title)
    return {"message": "Question file successfully updated"}


@app.delete("/questions")
def delete_questions(note_title):
    delete_all_questions(note_title)
    return {"message": "Questions succesfully deleted"}


# ==============================
# 📊 ANSWERS ENDPOINTS
# ==============================


@app.get("/answers")
def assess_answer(question_text, user_answer, question_response):
    evaluation = evaluate_answer(question_text, user_answer, question_response)
    if not evaluation:
        raise HTTPException(status_code=500, detail="Failed to assess answers")
    return evaluation


@app.post("/answers")
def save_quiz_results(note_title, question_text, user_answer, question_response, evaluation_score):

    save_quiz_result(
                        note_title,
                        question_text,
                        user_answer,
                        question_response,
                        evaluation_score
                    )
    return {"message": "Quiz results saved successfully"}

# ==============================
# 📊 STATS / PERFORMANCE
# ==============================

@app.get("/performances")
def get_all_performance_stats():
    return get_all_stats()


@app.get("/stats")
def calculate_overall_performances(stats: StatModel):
    all_scores = []
    notes_avg_scores = {}

    for note_title, note_stats in stats.stats.items():
        if note_stats["attempts"]:
            scores = [int(attempt["score"]) for attempt in note_stats["attempts"]]
            notes_avg_scores[note_title] = sum(scores) / len(scores)
            all_scores.extend(scores)

    return {"all_scores": all_scores, "notes_avg_scores": notes_avg_scores}


@app.delete("/performances")
def delete_note_stat(note_title):
   return delete_note_stats(note_title)


@app.delete("/performances")
def delete_all_stats_performances():
    return delete_all_stats()

