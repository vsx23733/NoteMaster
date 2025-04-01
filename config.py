import os
import secrets
# Folder where notes will be saved
NOTES_DIR = "./notes/"
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# Folder where questions will be saved
QUESTIONS_DIR = "./questions/"
if not os.path.exists(QUESTIONS_DIR):
    os.makedirs(QUESTIONS_DIR)

# User data base
USER_DB_DIR = "./db/user.json"

# Path of the file containing questions
QUESTIONS_FILE = os.path.join(QUESTIONS_DIR, "questions.json")

# URL of the API (fastapi)
BASE_URL = "http://127.0.0.1:8000"

# Authentication parameters
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


STATS_DIR = "./stats/"
if not os.path.exists(STATS_DIR):
    os.makedirs(STATS_DIR)
