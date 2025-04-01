import streamlit as st
import requests
import os
import json
from config import QUESTIONS_DIR, BASE_URL
from api_calls import *
st.title("📝 NoteMaster with FastAPI")

##################
# AUTHENTICATION #
##################

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None 

def login(username, password):
    """Authenticate user via FastAPI and store token."""
    response = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
    
    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["access_token"] 
        st.session_state.user = {"username": username, "email": data["email"]} 
        st.success(f"✅ Welcome, {st.session_state.user['username']}!")
        st.rerun() 
    else:
        st.error("🚫 Invalid credentials. Please try again.")

def signup(username, email, password):
    """Create a new user via FastAPI and store token."""
    response = requests.post(f"{BASE_URL}/auth/signup", 
                             json={"username": username, "email": email, "password": password}) 
    
    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["access_token"]
        st.session_state.user = {"username": username, "email": data["email"]}
        st.success(f"✅ Welcome, {st.session_state.user['username']}!")
        st.rerun()
    else:
        st.error(f"🚫 {response.json()['detail']}")

def logout():
    """Clear session on logout."""
    st.session_state.token = None
    st.session_state.user = None
    st.rerun()  

def edit_account(token, username, email):
    """Edit user account details via FastAPI."""
    url = f"{BASE_URL}/auth/edit-account"
    payload = {"username": username, "email": email, "token": token}
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        st.session_state.user = data
        st.success("✅ Account updated successfully!")
    else:
        st.error(f"🚫 {response.json()['detail']}")

def delete_account(token):
    """Delete user account via FastAPI."""
    url = f"{BASE_URL}/auth/delete-account"    
    response = requests.delete(url, json={"token": token})
    
    if response.status_code == 200:
        st.session_state.clear()  
        st.success("✅ Your account has been deleted.")
        st.experimental_rerun()
    else:
        st.error(f"🚫 {response.json()['detail']}")

if not st.session_state.token:
    st.sidebar.title("🔐 Login / Sign-Up")
    
    # Switch between login and signup form
    action = st.sidebar.radio("Choose an action", ["Login", "Sign Up"])
    
    if action == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            login(username, password)
    
    elif action == "Sign Up":
        username = st.sidebar.text_input("Username")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Sign Up"):
            signup(username, email, password)
    
    st.stop()

st.sidebar.title(f"👤 {st.session_state.user['username']}")
if st.sidebar.button("Logout"):
    logout()

    
###################
####### UI ########
###################


# st.sidebar.title("📝 **NoteMaster**")


st.markdown("""<style>
    /* Global styles */
    body {
        background-color: #121212; /* Dark background */
        font-family: 'Arial', sans-serif;
        color: #e0e0e0; /* Light text for readability */
    }

    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        color: #4CAF50; /* Green text for headings */
    }

    h1 {
        font-size: 2.5rem;
    }

    h2 {
        font-size: 2rem;
    }

    h3 {
        font-size: 1.5rem;
    }

    /* Sidebar Styles */
    .sidebar .sidebar-content {
        background-color: #1f1f1f; /* Dark background for the sidebar */
        color: #e0e0e0; /* Light text in the sidebar */
        border-right: 2px solid #333; /* Dark gray border */
    }

    .sidebar .sidebar-header {
        background-color: #1e2a3b; /* Dark blue background for sidebar header */
        color: white; /* White text */
        text-align: center;
        padding: 10px 0;
    }

    .sidebar .stRadio label {
        color: #4CAF50; /* Green text for radio labels */
    }

    /* Buttons */
    .stButton button {
        background-color: #4CAF50; /* Green button */
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #388E3C; /* Darker green on hover */
    }

    /* Cards or Sections */
    .stExpander {
        border-radius: 8px;
        border: 1px solid #4CAF50; /* Green border */
        padding: 10px;
        background-color: #2c2f36; /* Dark gray background */
    }

    /* Inputs */
    .stTextInput, .stTextArea {
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #4CAF50; /* Green border for inputs */
        box-sizing: border-box;
        background-color: #333333; /* Dark background for input fields */
        color: #e0e0e0; /* Light text in input fields */
    }

    .stTextInput input, .stTextArea textarea {
        font-family: 'Arial', sans-serif;
        font-size: 1rem;
        background-color: #333333; /* Dark background for text input */
        color: #e0e0e0; /* Light text */
    }

    /* Hover Effects on list items (notes) */
    .stButton:hover {
        background-color: #388E3C; /* Darker green on hover */
    }

    /* Title formatting */
    .stMarkdown h1 {
        color: #4CAF50; /* Green title */
        font-weight: bold;
        font-size: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""<style>
        .content {
            display: grid;
            grid-template-columns: 1fr 3fr;
            gap: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color: #4CAF50;'>Menu</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "📂 <span style='color: #4CAF50;'>Choisissez une option :</span>", 
    ["📊 Dashboard", "🗒️ Note-taking", "❓Quiz Mode", "📈📉 Performances", "📒 Docs"], 
    format_func=lambda x: f"{x}", 
    index=0,
    label_visibility="hidden", 
    key="menu_radio"
)

st.markdown(
    """
    <style>
        .css-1d391kg {
            background-color: #2c2f36; /* Dark background */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5);
        }
        .css-1d391kg:hover {
            background-color: #3a434a; /* Darker background on hover */
        }
        .css-1d391kg label {
            font-size: 18px;
            color: #4CAF50; /* Green text */
        }
    </style>
    """, unsafe_allow_html=True
)

# Main content
if menu == "📊 Dashboard":
    # Header with custom styles
    st.markdown("<h1>Welcome to NoteMaster ⚡️</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Learn with _Active Learning_!")


    st.markdown("""
    <style>
        body {
            background-color: #121212; /* Dark background */
            color: #E0E0E0; /* Light text for contrast */
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #00E676; /* Light green for emphasis */
        }
        .subtitle {
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            color: #76FF03; /* Lighter green */
        }
        .feature-box {
            background-color: #333333; /* Dark background for features */
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .emoji {
            font-size: 35px;
            color: #FFEB3B; /* Yellow for emojis */
        }
        .quote {
            font-size: 22px;
            font-style: italic;
            color: #BDBDBD; /* Light gray quote text */
            text-align: center;
            margin-top: 20px;
        }
        .highlight {
            color: #FF5722; /* Strong orange for highlighting */
            font-weight: bold;
        }
        .goal-section {
            background-color: #2C2C2C; /* Darker section background */
            padding: 30px;
            border-radius: 12px;
            margin-top: 20px;
        }
        .content-box {
            margin-top: 20px;
            text-align: justify;
            color: #E0E0E0; /* Lighter text inside the content box */
        }
        .feature-heading {
            font-size: 26px;
            font-weight: bold;
            color: #00B0FF; /* Light blue for feature headings */
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

    st.markdown('<p class="title">📖 Welcome to NoteMaster: The Ultimate Collaborative Learning Tool! 🚀</p>', unsafe_allow_html=True)

    st.markdown("""
        **NoteMaster** is an innovative learning platform designed to make education more interactive, engaging, and collaborative.  
        With the power of Artificial Intelligence and real-time student collaboration, NoteMaster enables students to **learn together** in a seamless and fun way.  
        Whether you're studying alone or with peers, NoteMaster ensures that you always have access to **interactive quizzes**, **real-time performance insights**, and the ability to **share notes** with others. 🌟
    """)

    st.markdown("""
    <style>
        .goal-section {
            background-color: #e1f5fe;
            padding: 30px;
            border-radius: 12px;
            margin-top: 20px;
            color: black; /* Ensures all text in goal-section is black */
        }
        .feature-heading {
            font-size: 26px;
            font-weight: bold;
            color: #009688;
            text-align: center;
        }
        .content-box {
            margin-top: 20px;
            text-align: justify;
            color: black; /* Ensures text inside content-box is also black */
        }
    </style>
    <div class="goal-section">
        <p class="feature-heading">🌍 Our Goal at NoteMaster 🌍</p>
        <div class="content-box">
            Our mission is simple: **to create an interactive, dynamic, and collaborative learning space** where students can easily learn, share, and grow. With NoteMaster, you can:  
            - 🧑‍🤝‍🧑 **Collaborate** with fellow students to exchange knowledge and insights.
            - 🔄 **Reinforce your learning** by reviewing notes, taking quizzes, and exploring new content continuously.  
            - 🧠 **Engage with AI-driven learning tools** that personalize your learning experience.
            - 📊 **Track and improve your performance** with real-time analytics.
        </div>
    </div>
""", unsafe_allow_html=True)

    # Key Features Section
    st.markdown('<p class="subtitle">✨ Key Features ✨</p>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box"><span class="emoji">📝</span> <b>Collaborative Learning & Note Sharing</b><br>In NoteMaster, collaboration is at the heart of the learning process. Students can share notes, view each other’s work, and collaborate on complex topics. This way, you can always **learn something new** from your peers and gain different perspectives on the material.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box"><span class="emoji">📊</span> <b>AI-Driven Performance Analysis</b><br>One of the key advantages of NoteMaster is its ability to help students understand their learning patterns. The **AI-powered performance dashboard** gives you insights into your strengths and areas that need improvement. It tracks your quiz performance, time spent on tasks, and even helps you set realistic goals.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box"><span class="emoji">🧠</span> <b>Interactive AI-Powered Quizzes</b><br>Quiz yourself with **AI-powered quizzes** that adapt to your learning progress. These quizzes analyze your strengths and weaknesses and **present personalized questions** that target areas where you need improvement. With **instant feedback** and detailed explanations, you can quickly grasp difficult concepts!</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box"><span class="emoji">🌍</span> <b>Learn & Interact with Peers in Real-Time</b><br>Engage with your classmates in **real-time** as you view and comment on each other’s notes. Share thoughts, ask questions, and **collaborate on learning tasks** together. Learning doesn’t have to be a solo journey—**make it social** and fun!</div>', unsafe_allow_html=True)
    st.markdown("""<div class="feature-box"><span class="emoji">⚡</span> <b>Instant AI Assistance</b><br>Need help with a difficult concept or stuck on a particular question? With **NoteMaster’s AI Assistant**, you can ask for real-time explanations and clarifications. Whether it's an entire chapter or a specific topic, the AI is there to help you **understand** the material in an easy-to-grasp way.</div>""", unsafe_allow_html=True)
    st.markdown("""
    <style>
        .black-text {
            color: black;
        }
        .feature-box {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            color: black; /* Ensures all text inside the feature-box is black */
        }
    </style>
    <div class="feature-box">
        <span class="emoji">📅</span> <b>Track Your Progress and Set Learning Goals</b><br>
        Stay on top of your learning journey by setting **personalized learning goals**. Track your progress over time with **AI-powered performance analytics**. See how well you're doing on quizzes, how often you’re reviewing your notes, and where you need to improve. This helps you stay motivated and aligned with your academic targets.
    </div>
""", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🧩 How NoteMaster Quizzes Work 🧩</p>', unsafe_allow_html=True)
    st.markdown("""
        **NoteMaster** quizzes are designed to be **adaptive and personalized**. Here’s how they work:  
        1. **Personalized Quiz Generation**: Based on your study history and notes, the AI generates quizzes tailored to your learning needs.  
        2. **Interactive Feedback**: After completing each question, the system provides immediate feedback, helping you understand why an answer is correct or incorrect.  
        3. **Progressive Difficulty**: As you continue to improve, the difficulty level of the questions gradually increases, keeping you challenged without overwhelming you.  
        4. **Score Analytics**: After completing a quiz, receive a detailed report on your performance, including areas to focus on for improvement.
    """)
    st.markdown("""
        <p class="quote">"Learning is more fun when you're engaged, connected, and growing together. Join NoteMaster today and take your education to the next level!"</p>
        **Ready to make the most of your learning journey?**  
        With **NoteMaster**, you can collaborate, engage, and **track your learning progress** like never before. It's time to **accelerate your education** and experience the future of learning today. 🚀💡  
        Click below to get started with **NoteMaster** and unlock a world of possibilities!
    """, unsafe_allow_html=True)


elif menu == "🗒️ Note-taking":
    st.header("Note-taking")

    if "notes" not in st.session_state:
        st.session_state.notes = fetch_notes() # API call function here

    if "editing_note" not in st.session_state:
        st.session_state.editing_note = None

    # Displaying existing notes

    st.write("### Your notes :")
    if st.session_state.notes:
        for note in st.session_state.notes:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📝 {note['title']}")
            with col2:
                if st.button("View/Edit", key=f"edit_{note['title']}"):
                    st.session_state.editing_note = note
            with col3:
                if st.button("Delete", key=f"delete_{note['title']}"):
                    delete_note(note['title']) # API call to delete the note
                    st.session_state.notes = fetch_notes() # API call to refresh the fetching
                    if st.session_state.editing_note and st.session_state.editing_note['title'] == note['title']:
                        st.session_state.editing_note = None
                    st.rerun()
    else:
        st.info("No notes available at the moment.")

    # Editing/viewing section
    if st.session_state.editing_note: # Retrieve the note to edit
        st.markdown("---")
        st.subheader(f"Modify note : {st.session_state.editing_note['title']}")
        edited_content = st.text_area(
            "Note content",
            value=st.session_state.editing_note['content'],
            height=300,
            key="edit_content"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save changes"):
                if update_note(st.session_state.editing_note['title'], edited_content): # API call for editing notes
                    st.success("Note successfully updated!")
                    st.session_state.notes = fetch_notes()
                    st.session_state.editing_note = None
                    st.rerun()
                else:
                    st.error("Error updating note")
        with col2:
            if st.button("Cancel"):
                st.session_state.editing_note = None
                st.rerun()

    # Section to create a new note
    st.markdown("---")
    st.subheader("Create a new note")
    note_title = st.text_input("Note title")
    note_content = st.text_area("Note content", height=200)

    if st.button("Save"):
        if note_title and note_content:
            save_note(note_title, note_content)
            st.session_state.notes = fetch_notes()
            st.success(f"Note '{note_title}' sauvegardée avec succès !")
            st.rerun()
        else:
            st.warning("Please provide a title and content for your note.")


elif menu == "❓Quiz Mode":

    st.header("Quiz Mode")

    # Load available notes
    notes = fetch_notes()
    note_titles = [note["title"] for note in notes]
    selected_note = st.selectbox("Select a note", note_titles)

    if selected_note:
        note_content = next(note["content"] for note in notes if note["title"] == selected_note)
        json_file_path = os.path.join(QUESTIONS_DIR, f"{selected_note}.json")

        # Question initialization
        if "questions" not in st.session_state or st.session_state.get("current_note") != selected_note:
            st.session_state.questions = load_question(selected_note) # API call to load questions specific to a certain course
            st.session_state.current_note = selected_note

            # Initialize a dictionary to store answers
            st.session_state.user_answers = {}

        # Generate new questions
        if st.button("Generate questions"):
            try:
                with st.spinner("Generation of current questions..."):
                    new_questions = generate_questions(selected_note, note_content) # API call to generate questions 
                
                if new_questions:
                    # update_questions_file(new_questions, selected_note)
                    
                    # with open(json_file_path, "w") as file:
                    #    json.dump(new_questions, file, indent=4, ensure_ascii=False)
                    
                    st.session_state.questions = new_questions
                    st.session_state.user_answers = {}  # Reset answers
                    st.success("Questions successfully generated and saved!")
                else:
                    st.error("API returned no questions.")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

        # Show questions
        if st.session_state.questions:
            st.write("### Questions :")
            
            # Display all questions with answer fields
            for i, question in enumerate(st.session_state.questions, 1):
                st.write(f"**Question {i}:** {question['text']}")
                # Store response in session_state
                answer_key = f"answer_{i}"
                user_answer = st.text_area(
                    "Your answer",
                    key=answer_key,
                    height=100
                )
                st.session_state.user_answers[answer_key] = user_answer
                st.markdown("---")

        # Single button to check all answers
            if st.button("📝 Check all answers"):
                total_score = 0
                with st.spinner("Evaluation of current responses..."):
                    for i, question in enumerate(st.session_state.questions, 1):
                        answer_key = f"answer_{i}"
                        user_answer = st.session_state.user_answers.get(answer_key, "")

                        # Evaluating the response
                        evaluation = evaluate_answer(
                            question['text'],
                            user_answer,
                            question['reponse']
                        )

                        # Save result
                        save_quiz_result(
                            selected_note,
                            question['text'],
                            user_answer,
                            question['reponse'],
                            evaluation['score']
                        )

                        total_score += evaluation['score']

                        # Show result for this question
                        with st.expander(f"Result Question {i}"):
                            st.write(f"**Your answer:** {user_answer}")
                            st.write(f"**Correct answer:** {question['reponse']}")
                            st.write(f"**Score:** {evaluation['score']}/5")

                # Display total score
                avg_score = total_score / len(st.session_state.questions)
                st.success(f"Total score : {avg_score:.1f}/5")

                # Option to restart
                if st.button("🔄 Start quiz again"):
                    st.session_state.user_answers = {}
                    st.rerun()

        # Button for deleting questions
            if st.button("🗑️ Delete all questions"):
                try:
                    delete_all_question(selected_note)
                    st.session_state.questions = []
                    st.session_state.user_answers = {}
                    st.success("The questions have been successfully removed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Deletion error : {e}")
        
        else:
            st.info("No questions available. Click on 'Generate questions' to start.")


elif menu == "📈📉 Performances":
    st.header("📊 Learning performance")

    stats = get_all_stats()
    if not stats:
        st.info("No statistics available yet. Start taking quizzes to see how you're doing!")
    else:
        # Global overview
        st.subheader("Vue d'ensemble")

        # Calculate overall statistics
        all_scores, notes_avg_scores = compute_overall_performance(stats)

        # Display overall average score
        if all_scores:
            global_avg = sum(all_scores) / len(all_scores)
            st.metric("Overall average score", f"{global_avg:.1f}/5")
            
            # Graph of average scores by note
            st.bar_chart(notes_avg_scores)

        # Details by note
        st.subheader("Details by note")
        for note_title, note_stats in stats.items():
            with st.expander(f"📝 {note_title}"):
                if note_stats["attempts"]:
                    col1, col2, col3 = st.columns(3)
                    
                    # Basic statistics
                    scores = [int(attempt["score"]) for attempt in note_stats["attempts"]]
                    avg_score = sum(scores) / len(scores)
                    with col1:
                        st.metric("Average score", f"{avg_score:.1f}/5")
                    with col2:
                        st.metric("Best score", f"{max(scores)}/5")
                    with col3:
                        st.metric("Number of questions", len(scores))
                    
                    # Score evolution graph
                    scores_df = {
                        "Question": range(1, len(scores) + 1),
                        "Score": scores
                    }
                    st.line_chart(scores_df, x="Question", y="Score")
                    
                    # Detailed history
                    st.markdown("<h3 style='color: #0044CC;'>Detailed history</h3>", unsafe_allow_html=True)
                    for attempt in reversed(note_stats["attempts"]):
                        st.markdown(f"""
                            <div style="background-color: #333; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                                <p style="font-size: 14px; color: #fff;">
                                    <strong>📅 {attempt['timestamp'][:16].replace('T', ' à ')}</strong><br>
                                    <strong>Question:</strong> {attempt['question']}<br>
                                    <strong>Your answer:</strong> {attempt['user_answer']}<br>
                                    <strong>Correct answer:</strong> {attempt['correct_answer']}<br>
                                    <strong>Score:</strong> {attempt['score']}/5
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Button to delete the history of this note
                    if st.button("🗑️ Delete history", key=f"delete_{note_title}"):
                        if delete_note_stats(note_title):
                            st.success(f"History deleted for {note_title}")
                            st.rerun()
                        else:
                            st.error("Error deleting history")

        # Button to delete all history
        st.markdown("---")
        if st.button("🗑️ Delete all history", type="secondary"):
            if delete_all_stats():
                st.success("All history deleted")
                st.rerun()
            else:
                st.error("Error deleting history")

elif menu == "📒 Docs":
    st.header("📖 Docs")

    # Documentation on Deepseek's API via OpenRouter 
    st.subheader("Configure Deepseek's API via OpenRouter")
    st.markdown(
        """
        To use the DeepSeek API in this application, you need to generate an OpenRouter API key and configure it. Two options are available:

        ### 1️⃣ Get an OpenRouter API key
        - Go to [OpenRouter](https://openrouter.ai) and create an account.
        - Generate a free API key for the DeepSeek V3 model.

        ### 2️⃣ Add your API key to the application

        **Option 1: via a `.env` file (manual)**
        - Create an `.env` file at the root of the project.
        - Add the following line, replacing `YOUR_API_KEY` with your API key:
          ```
          DEEPSEEK_KEY=YOUR_API_KEY
          ```
        - Restart the application for the changes to take effect:
          ```bash
          streamlit run app.py
          ```

        ### 💡 Troubleshooting
        If you encounter problems with the API:
        - Check that your API key is correct and valid.
        - Make sure you have installed the necessary dependencies (`pip install openai`).
        - Consult the OpenRouter documentation here: [OpenRouter documentation](https://openrouter.ai/docs)
        """
    )
    


