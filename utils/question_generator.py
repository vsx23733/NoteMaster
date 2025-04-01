import os
import re
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from config import QUESTIONS_DIR, QUESTIONS_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# API configuration
# api_key = os.getenv("DEEPSEEK_KEY")
api_key = "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" 

if not api_key:
    raise ValueError("DEEPSEEK_KEY environment variable is not set!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def load_question(title):
    json_file_path = os.path.join(QUESTIONS_DIR, f"{title}.json")
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            questions = json.load(file)
    else:
        questions = []
    return questions

def update_questions(new_questions, title):
    json_file_path = os.path.join(QUESTIONS_DIR, f"{title}.json")
    if os.path.exists(json_file_path):
        with open(json_file_path, "w") as file:
            json.dump(new_questions, file, indent=4, ensure_ascii=False)


def delete_all_questions(title):
    json_file_path = os.path.join(QUESTIONS_DIR, f"{title}.json")
    with open(json_file_path, "w") as file:
        json.dump("details", file, indent=4, ensure_ascii=False)


def generate_questions(note_title, note_content):
    """
    Generates questions from note content using the DeepSeek API.
    :param note_title: Note title
    :param note_content: Note content
    :return: A list of generated questions
    """
    try:
        prompt = (
            f"From this text, create relatively open-ended questions that allow for active learning.\n"
            f"Choose the right number of questions for the length of the text.\n"
            f"For each question, return a JSON with two keys: "
            f"text' for the question and 'reponse' for the correct answer.\n"
            f"Text : {note_content}\n"
            f"Returns JSON only, nothing else."
        )

        # Send request to API
        response = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # Checking the answer
        logging.info("Raw API response : %s", response)
        generated_text = response.choices[0].message.content.strip()
        if generated_text.startswith("```json") and generated_text.endswith("```"):
            generated_text = generated_text.strip("```json").strip("```")
        if not generated_text:
            raise ValueError("Empty response returned by the API.")

        # Loading JSON
        try:
            questions = json.loads(generated_text)
        except json.JSONDecodeError as json_err:
            logging.error("Error parsing JSON : %s", json_err)
            raise ValueError("The API response is not a valid JSON.")

        # Save questions in a JSON file
        json_file_path = os.path.join(QUESTIONS_DIR, f"{note_title}.json")
        with open(json_file_path, "w") as file:
            json.dump(questions, file, indent=4, ensure_ascii=False)
        logging.info("Questions saved in : %s", json_file_path)
        return questions

    except Exception as e:
        logging.error("Error when generating questions : %s", e)
        return []

def save_questions(questions):
    """
    Saves generated questions in a JSON file.
    :param questions: List of questions
    """
    try:
        if not os.path.exists(os.path.dirname(QUESTIONS_FILE)):
            os.makedirs(os.path.dirname(QUESTIONS_FILE))
        with open(QUESTIONS_FILE, "w") as file:
            json.dump(questions, file, indent=4)
        logging.info("Questions saved in the main file : %s", QUESTIONS_FILE)
    except Exception as e:
        logging.error("Error saving questions : %s", e)

def load_questions():
    """
    Loads saved questions from JSON file.
    :return: List of questions
    """
    try:
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, "r") as file:
                return json.load(file)
    except Exception as e:
        logging.error("Error loading questions : %s", e)
    return []

def evaluate_answer(question, user_answer, correct_answer):
    """
    Evaluates user response using the API
    """
    try:
        prompt = (
            f"You're a teacher who evaluates a student's response in a caring way.\n"
            f"Question: {question}\n"
            f"Correct answer: {correct_answer}\n"
            f"Student response: {user_answer}\n\n"
            f"Valuation rules:\n"
            f"- A short answer that contains the essential elements deserves a very good mark.\n"
            f"- If the main keywords are present, the score should be high (4 or 5).\n"
            f"- The form of the answer is less important than the content\n"
            f"- A concise, precise answer is worth as much as a detailed one\n\n"
            f"Returns ONLY a valid JSON with this exact format: {{\"score\": X}} where X is a number between 0 and 5.\n"
            f"Use double quotes for the key \"score\"."
        )

        response = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
        )

        if not response or not response.choices:
            raise ValueError("The API did not return any valid choices.")

        raw_content = response.choices[0].message.content
        if not raw_content:
            raise ValueError("The API response is empty.")

        # More robust JSON cleaning
        cleaned_content = re.sub(r"^```json\s*|\s*```$", "", raw_content.strip(), flags=re.MULTILINE)
        
        # Correction of single quotation marks to double if necessary
        cleaned_content = cleaned_content.replace("'", '"')
        
        try:
            evaluation = json.loads(cleaned_content)
        except json.JSONDecodeError:
            # If parsing fails, attempt to correct format
            score_match = re.search(r'score["\']?\s*:\s*(\d+)', cleaned_content)
            if score_match:
                return {"score": int(score_match.group(1))}
            raise

        if "score" not in evaluation:
            raise ValueError("The JSON returned does not contain the key 'score'.")

        return {"score": evaluation["score"]}

    except Exception as e:
        logging.exception("Error in response evaluation")
        return {"score": 0}