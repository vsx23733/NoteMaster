import streamlit as st

st.set_page_config(
    page_title="NoteMaster",
    page_icon="📝",
    layout="wide"
)

import os, json
from utils.note_manager import load_notes, save_note, delete_note, update_note
from utils.question_generator import generate_questions, evaluate_answer
from config import QUESTIONS_DIR
from utils.stats_manager import get_all_stats, save_quiz_result, delete_note_stats, delete_all_stats

# Main application

# Sidebar 
st.sidebar.title("📝 **NoteMaster**")
st.sidebar.markdown("<h3>Menu</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "📂 <span style='color: #0066CC;'>Choisissez une option :</span>", 
    ["Dashboard", "Note-taking", "Quiz mode", "Performances", "API", "Docs"], 
    format_func=lambda x: f"🔹 {x}", 
    index=0,
    label_visibility="hidden", 
    key="menu_radio"
)

# Main content
if menu == "Dashboard":
    # Header with custom styles
    st.markdown("<h1>Welcome to NoteMaster ⚡️</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Learn with _Active Learning_!")

    # Feature list with emojis and custom formatting
    st.markdown(
        """
        <div style='padding: 10px;'>
            <p><strong>NoteMaster</strong> allows you to :</p>
            <ul>
                <li>🗒️ <strong>Taking notes</strong> and organize them.</li>
                <li>❓ <strong>Generate questions</strong> for your courses.</li>
                <li>✅ <strong>Active learning</strong> and track your progress.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )


elif menu == "Note-taking":
    st.header("Note-taking")
    
    if "notes" not in st.session_state:
        st.session_state.notes = load_notes()
    
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
                    delete_note(note['title'])
                    st.session_state.notes = load_notes()
                    if st.session_state.editing_note and st.session_state.editing_note['title'] == note['title']:
                        st.session_state.editing_note = None
                    st.rerun()
    else:
        st.info("No notes available at the moment.")

    # Editing/viewing section
    if st.session_state.editing_note:
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
                if update_note(st.session_state.editing_note['title'], edited_content):
                    st.success("Note successfully updated!")
                    st.session_state.notes = load_notes()
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
            st.session_state.notes = load_notes()
            st.success(f"Note '{note_title}' sauvegardée avec succès !")
            st.rerun()
        else:
            st.warning("Please provide a title and content for your note.")



elif menu == "Quiz Mode":
    st.header("Quiz Mode")
    
    # Load available notes
    notes = load_notes()
    note_titles = [note["title"] for note in notes]
    selected_note = st.selectbox("Select a note", note_titles)

    if selected_note:
        note_content = next(note["content"] for note in notes if note["title"] == selected_note)
        json_file_path = os.path.join(QUESTIONS_DIR, f"{selected_note}.json")
        
        # Question initialization
        if "questions" not in st.session_state or st.session_state.get("current_note") != selected_note:
            if os.path.exists(json_file_path):
                with open(json_file_path, "r") as file:
                    st.session_state.questions = json.load(file)
            else:
                st.session_state.questions = []
            st.session_state.current_note = selected_note
            # Initialize a dictionary to store answers
            st.session_state.user_answers = {}

        # Generate new questions
        if st.button("Generate questions"):
            try:
                with st.spinner("Generation of current questions..."):
                    new_questions = generate_questions(selected_note, note_content)
                
                if new_questions:
                    with open(json_file_path, "w") as file:
                        json.dump(new_questions, file, indent=4, ensure_ascii=False)
                    
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
                    os.remove(json_file_path)
                    st.session_state.questions = []
                    st.session_state.user_answers = {}
                    st.success("The questions have been successfully removed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Deletion error : {e}")
        
        else:
            st.info("No questions available. Click on 'Generate questions' to start.")


elif menu == "Performances":
    st.header("📊 Learning performance")
    
    stats = get_all_stats()
    if not stats:
        st.info("No statistics available yet. Start taking quizzes to see how you're doing!")
    else:
        # Global overview
        st.subheader("Vue d'ensemble")
        
        # Calculate overall statistics
        all_scores = []
        notes_avg_scores = {}
        for note_title, note_stats in stats.items():
            if note_stats["attempts"]:
                scores = [attempt["score"] for attempt in note_stats["attempts"]]
                notes_avg_scores[note_title] = sum(scores) / len(scores)
                all_scores.extend(scores)
        
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
                    scores = [attempt["score"] for attempt in note_stats["attempts"]]
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
                    st.write("### Detailed history")
                    for attempt in reversed(note_stats["attempts"]):
                        st.markdown(f"""
                        **📅 {attempt['timestamp'][:16].replace('T', ' à ')}**
                        - **Question:** {attempt['question']}
                        - **Your answer:** {attempt['user_answer']}
                        - **Correct answer:** {attempt['correct_answer']}
                        - **Score:** {attempt['score']}/5
                        ---
                        """)
                    
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


elif menu == "API":
    st.header("API configuration")

    # Load existing API key (if any)
    if "api_key" not in st.session_state:
        from dotenv import load_dotenv
        load_dotenv()
        st.session_state.api_key = os.getenv("DEEPSEEK_KEY", "")

    # Form to enter or update API key
    st.write("Enter your OpenRouter API key to activate the generation functions.")
    api_key_input = st.text_input(
        "Clé API",
        value=st.session_state.api_key,
        placeholder="Enter your API key",
        type="password",
        key="api_input"
    )

    # Save or reset buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register API key"):
            if len(api_key_input) == 73:
                with open(".env", "w") as file:
                    file.write(f'DEEPSEEK_KEY="{api_key_input}"')
                st.session_state.api_key = api_key_input
                st.success("API key successfully registered!")
            else:
                st.error("Invalid API key. It must be exactly 73 characters long.")

    with col2:
        if st.button("Reset API key"):
            if os.path.exists(".env"):
                os.remove(".env")
            st.session_state.api_key = ""
            st.warning("API key reset. Please enter a new one.")


elif menu == "Docs":
    st.header("📖 Docs")

    # Documentation on Deepseek's API via OpenRouter 
    st.subheader("Configurer l'API DeepSeek V3 via OpenRouter")
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
    
# Divider
st.markdown("---")

