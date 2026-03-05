import streamlit as st
import random

# --- APP SETUP ---
st.set_page_config(page_title="The Culture Quote Quiz", page_icon="🎬")

# --- MOVIE DATA ---
# Based on your facts
quiz_data = [
    {"quote": "Surely you can't be serious. / I am serious... and don't call me Shirley.", "options": ["Airplane!", "Coming to America", "Friday"], "answer": "Airplane!"},
    {"quote": "The royal penis is clean, your Highness.", "options": ["Coming to America", "Boomerang", "New Jack City"], "answer": "Coming to America"},
    {"quote": "Don’t nobody go in the bathroom for about 35, 45 minutes.", "options": ["Friday", "Do the Right Thing", "Training Day"], "answer": "Friday"},
    {"quote": "King Kong ain't got shit on me!", "options": ["Training Day", "Black Panther", "The Woman King"], "answer": "Training Day"},
    {"quote": "I am your wife! I am the greatest good you are ever gonna get!", "options": ["The Incredibles", "Princess and the Frog", "The Wiz"], "answer": "The Incredibles"},
    {"quote": "Wakanda Forever!", "options": ["Black Panther", "Origin", "The Book of Clarence"], "answer": "Black Panther"},
    {"quote": "Heritage isn't just what was left for us; it’s what we build for them.", "options": ["Horizon: The New World", "The Woman King", "Fade to Black"], "answer": "Horizon: The New World"},
    {"quote": "Love should've brought your ass home last night.", "options": ["Boomerang", "Friday", "Coming to America"], "answer": "Boomerang"},
    {"quote": "Always do the right thing.", "options": ["Do the Right Thing", "New Jack City", "The Fresh Prince"], "answer": "Do the Right Thing"},
    {"quote": "I’m not a businessman; I’m a business, man.", "options": ["Fade to Black", "Training Day", "The Fast and the Furious"], "answer": "Fade to Black"}
]

# --- SESSION STATE ---
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

def next_question(selected):
    if selected == quiz_data[st.session_state.quiz_step]['answer']:
        st.session_state.score += 1
    st.session_state.quiz_step += 1

def restart_quiz():
    st.session_state.quiz_step = 0
    st.session_state.score = 0

# --- APP LOGIC ---
st.title("🎬 The Culture Quote Quiz")

if st.session_state.quiz_step < len(quiz_data):
    current = quiz_data[st.session_state.quiz_step]
    
    st.subheader(f"Question {st.session_state.quiz_step + 1} of {len(quiz_data)}")
    st.info(f"\"{current['quote']}\"")
    
    # User selects answer
    choice = st.radio("Which movie is this from?", current['options'])
    
    if st.button("Submit Answer"):
        next_question(choice)
        st.rerun()

else:
    # --- FINAL GRADE LOGIC ---
    total = len(quiz_data)
    final_score = st.session_state.score
    percent = (final_score / total) * 100
    
    st.header("🏁 Quiz Complete!")
    
    if percent >= 90:
        grade, meaning = "A", "Ancestor Approved! You are a legend."
    elif percent >= 80:
        grade, meaning = "B", "Blockbuster Buff. You know your stuff!"
    elif percent >= 70:
        grade, meaning = "C", "Cousin Status. You're invited to the cookout, but stay by the grill."
    elif percent >= 60:
        grade, meaning = "D", "Director’s Cut. You need a movie marathon, fam."
    else:
        grade, meaning = "F", "First Time? 'Bye, Felicia!'"

    st.subheader(f"Your Grade: {grade}")
    st.write(meaning)
    st.progress(percent / 100)
    st.write(f"You got {final_score} out of {total} correct.")

    if st.button("🔄 Try Again"):
        restart_quiz()
        st.rerun()