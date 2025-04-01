import os
from config import NOTES_DIR  

def load_notes():
    notes = []
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(NOTES_DIR, filename), "r") as file:
                notes.append({"title": filename.replace(".txt", ""), "content": file.read()})
    return notes

def save_note(title, content):
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
    with open(os.path.join(NOTES_DIR, f"{title}.txt"), "w") as file:
        file.write(content)

def delete_note(title):
    filepath = os.path.join(NOTES_DIR, f"{title}.txt")
    if os.path.exists(filepath):
        os.remove(filepath)

def update_note(title, new_content):
    """
    Updates the content of an existing note
    :param title: Note title
    :param new_content: New content
    :return: True if update successful, False otherwise
    """
    filepath = os.path.join(NOTES_DIR, f"{title}.txt")
    if os.path.exists(filepath):
        with open(filepath, "w") as file:
            file.write(new_content)
        return True
    return False
