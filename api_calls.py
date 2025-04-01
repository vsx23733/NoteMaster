from config import BASE_URL
import requests
import streamlit as st


# Notes API calls
def fetch_notes():
    response = requests.get(f"{BASE_URL}/notes")
    return response.json() if response.status_code == 200 else []

def save_note(title, content):
    response = requests.post(f"{BASE_URL}/notes", params={"title": title, "content": content})
    return response.json()

def delete_note(title):
    response = requests.delete(f"{BASE_URL}/notes", params={"title": title})
    return response.json()

def update_note(title, content):
    response = requests.put(f"{BASE_URL}/notes", params={"title": title, "content": content})
    return response.json()

# Question API Calls
def load_question(note_title):
    response = requests.get(f"{BASE_URL}/questions", params={"title": note_title})
    if response.status_code != 200:
        raise Exception(f"Error fetching questions: {response.status_code} - {response.text}")
    return response.json()

def generate_questions(note_tile, note_content):
    response = requests.post(f"{BASE_URL}/questions", json={"note_title": note_tile, "note_content": note_content})
    return response.json()

def update_questions_file(new_question, note_title):
    response = requests.put(f"{BASE_URL}/questions", params={"new_questions": new_question, "note_title": note_title})
    return response.json()

def delete_all_question(note_title):
    response = requests.delete(f"{BASE_URL}/questions", params={"note_title": note_title})
    return response.json()


# Answers API calls
def evaluate_answer(question_text, user_answer, question_response):
    response = requests.get(f"{BASE_URL}/answers", params={"question_text": question_text, "user_answer": user_answer, "question_response": question_response})
    return response.json()

def save_quiz_result(note_title, question_text, user_answer, question_response, evaluation_score):
    response = requests.post(f"{BASE_URL}/answers", params={"note_title": note_title, "question_text": question_text, 
                                                            "user_answer": user_answer, "question_response": question_response, 
                                                            "evaluation_score": evaluation_score})
    return response.json()


# Stats/Performances API calls
def get_all_stats():
    response = requests.get(f"{BASE_URL}/performances")
    return response.json() 

def compute_overall_performance(stats):
    response = requests.get(f"{BASE_URL}/stats", json={"stats": stats})
    data = response.json()
    print("API Response:", data) 
    return data["all_scores"], data["notes_avg_scores"]

def delete_note_stats(note_title):
    response = requests.delete(f"{BASE_URL}/performances", params={"note_title": note_title})
    return response.json()

def delete_all_stats():
    response = requests.delete(f"{BASE_URL}/performances")
    return response.json()    