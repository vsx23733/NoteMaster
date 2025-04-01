import os
import json
from datetime import datetime
from config import STATS_DIR
import logging

def save_quiz_result(note_title, question_text, user_answer, correct_answer, score):
    """
    Save the result of a quiz question
    """
    if not os.path.exists(STATS_DIR):
        os.makedirs(STATS_DIR)
        
    stats_file = os.path.join(STATS_DIR, f"{note_title}_stats.json")
    
    # Load existing stats or create a new dictionary
    if os.path.exists(stats_file):
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    else:
        stats = {"attempts": []}
    
    # Add new attempt
    attempt = {
        "timestamp": datetime.now().isoformat(),
        "question": question_text,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "score": score
    }
    
    stats["attempts"].append(attempt)
    
    # Sauvegarder les stats
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

def get_note_stats(note_title):
    """
    Retrieves statistics for a given note
    """
    stats_file = os.path.join(STATS_DIR, f"{note_title}_stats.json")
    if os.path.exists(stats_file):
        with open(stats_file, 'r') as f:
            return json.load(f)
    return {"attempts": []}

def get_all_stats():
    """
    Retrieves all statistics
    """
    all_stats = {}
    if os.path.exists(STATS_DIR):
        for filename in os.listdir(STATS_DIR):
            if filename.endswith('_stats.json'):
                note_title = filename.replace('_stats.json', '')
                with open(os.path.join(STATS_DIR, filename), 'r') as f:
                    all_stats[note_title] = json.load(f)
    return all_stats

def delete_note_stats(note_title):
    """
    Delete stats history for a given note
    """
    stats_file = os.path.join(STATS_DIR, f"{note_title}_stats.json")
    try:
        if os.path.exists(stats_file):
            os.remove(stats_file)
            return True
    except Exception as e:
        logging.error(f"Error deleting stats from {note_title}: {e}")
    return False

def delete_all_stats():
    """
    Supprime tout l'historique des stats
    """
    try:
        if os.path.exists(STATS_DIR):
            for filename in os.listdir(STATS_DIR):
                if filename.endswith('_stats.json'):
                    os.remove(os.path.join(STATS_DIR, filename))
            return True
    except Exception as e:
        logging.error(f"Error deleting all stats: {e}")
    return False 