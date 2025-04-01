# 📝 NoteMaster with FastAPI

NoteMaster is a powerful and user-friendly note-taking application built using FastAPI and Streamlit. It allows users to create, manage, and analyze their notes efficiently. The app also provides AI-generated questions to help users retain information effectively.
The purpose of this app is to help users learn actively using AI in a simple but efficient way but also to learn from each and other insights.
The subjects that one user create with the question and answers associated aren't private so as allow other users to learn that also and then improve their knowledge somehow with the help of other users also.
This is one of the first open-collaborative learning platform.

## 🚀 Features

- **FastAPI Backend:** Provides a robust and scalable API for managing notes and user authentication.
- **Streamlit Frontend:** A simple and interactive UI for easy access to notes and quizzes.
- **User Authentication:** Secure login system with token-based authentication.
- **Question Generation:** AI-powered question generation based on notes.
- **Quiz and Evaluation:** Evaluate answers and track learning progress.
- **Statistics Dashboard:** Get insights into learning progress and note usage.

## 📌 Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- pip (Python package manager)

### Clone the Repository
```sh
$ git clone https://github.com/vsx23733/NoteMaster.git
$ cd NoteMaster
```

### Install Dependencies
```sh
$ pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file in the root directory and add the following:
```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BASE_URL=http://127.0.0.1:8000
```

## 🔧 Running the Application

### Start the FastAPI Backend
```sh
$ uvicorn src.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### Start the Streamlit Frontend
```sh
$ streamlit run src/notemaster.py
```
This will launch the web app in your default browser.

## 📡 API Endpoints

### Authentication
- `POST /token` - Authenticate user and receive a token.
- `POST /register` - Register a new user.

### Notes Management
- `GET /notes` - Retrieve all notes.
- `POST /notes` - Create a new note.
- `PUT /notes/{note_id}` - Update a note.
- `DELETE /notes/{note_id}` - Delete a note.

### Quiz and Evaluation
- `GET /questions` - Fetch generated questions.
- `POST /evaluate` - Evaluate quiz answers.

## 🤝 Contributing

I welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## 🎯 Next imrprovements

1. Adding more insights and detailed analysis of the answer
2. Organizing the notes per subjects
3. Improve the UI
4. Link to an online Database
5. Deploy on web

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
