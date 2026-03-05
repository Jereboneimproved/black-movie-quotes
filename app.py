import streamlit as st
import google.generativeai as genai
import random
import pandas as pd

# --- CLOUD CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")

# --- APP SETUP ---
st.set_page_config(page_title="The Culture Quote Quiz", page_icon="🎬")

# Initialize Leaderboard & Quiz State
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'hint' not in st.session_state:
    st.session_state.hint = ""

# --- MOVIE DATA ---
quiz_data = [
    {"quote": "Surely you can't be serious. / I am serious... and don't call me Shirley.", "options": ["Airplane!", "Coming to America", "Friday"], "answer": "Airplane!", "actor": "Kareem Abdul-Jabbar"},
    {"quote": "The royal penis is clean, your Highness.", "options": ["Coming to America", "Boomerang", "New Jack City"], "answer": "Coming to America", "actor": "The Bathers"},
    {"quote": "Don’t nobody go in the bathroom for about 35, 45 minutes.", "options": ["Friday", "Do the Right Thing", "Training Day"], "answer": "Friday", "actor": "Bernie Mac"},
    {"quote": "King Kong ain't got shit on me!", "options": ["Training Day", "Black Panther", "The Woman King"], "answer": "Training Day", "actor": "Denzel Washington"},
    {"quote": "I am your wife! I am the greatest good you are ever gonna get!", "options": ["The Incredibles", "Princess and the Frog", "The Wiz"], "answer": "The Incredibles", "actor": "Honey Best"},
    {"quote": "Wakanda Forever!", "options": ["Black Panther", "Origin", "The Book of Clarence"], "answer": "Black Panther", "actor": "Chadwick Boseman"},
    {"quote": "Love should've brought your ass home last night.", "options": ["Boomerang", "Friday", "Coming to America"], "answer": "Boomerang", "actor": "Grace Jones"},
    {"quote": "Always do the right thing.", "options": ["Do the Right Thing", "New Jack City", "The Fresh Prince"], "answer": "Do the Right Thing", "actor": "Da Mayor"},
    {"quote": "I’m not a businessman; I’m a business, man.", "options": ["Fade to Black", "Training Day", "The Fast and the Furious"], "answer": "Fade to Black", "actor": "Jay-Z"}
]

st.title("🎬 The Culture Quote Quiz")

# --- QUIZ INTERFACE ---
if st.session_state.quiz_step < len(quiz_data):
    current = quiz_data[st.session_state.quiz_step]
    st.subheader(f"Question {st.session_state.quiz_step + 1} of {len(quiz_data)}")
    st.info(f"\"{current['quote']}\"")
    
    if st.button("💡 Need a Hint?"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Give a funny, cryptic 1-sentence hint for the movie quote '{current['quote']}' featuring '{current['actor']}'. Don't name the movie. Use 'cookout' vibes."
            response = model.generate_content(prompt)
            st.session_state.hint = response.text
        except:
            st.session_state.hint = "You definitely saw this one at the cookout."
            
    if st.session_state.hint:
        st.write(f"*{st.session_state.hint}*")

    choice = st.radio("Choose the correct movie:", current['options'])
    
    if st.button("Submit Answer 🎯"):
        if choice == current['answer']:
            st.session_state.score += 1
        st.session_state.quiz_step += 1
        st.session_state.hint = ""
        st.rerun()

# --- RESULTS & LEADERBOARD ---
else:
    total = len(quiz_data)
    score = st.session_state.score
    percent = (score / total) * 100
    
    if percent >= 90: grade, desc = "A", "Ancestor Approved"
    elif percent >= 80: grade, desc = "B", "Blockbuster Buff"
    elif percent >= 70: grade, desc = "C", "Cousin Status"
    elif percent >= 60: grade, desc = "D", "Director’s Cut"
    else: grade, desc = "F", "First Time?"

    st.header(f"🏁 Your Final Grade: {grade}")
    if grade == "A":
        st.balloons()
        st.success(f"🏆 {desc}! You are the keeper of the culture.")

    # SHARE BUTTON
    share_text = f"I just got a Grade {grade} ({desc}) on the Culture Quote Quiz! My score: {score}/{total}. Can you beat me? 🎬🔥"
    st.text_area("Copy this to your group chat:", value=share_text, height=70)

    # GRADING TABLE
    st.write("### 📜 What does your grade mean?")
    st.markdown("""
    | Grade | Meaning | Vibe |
    | :--- | :--- | :--- |
    | **A** | **Ancestor Approved** | You are the keeper of the culture. |
    | **B** | **Blockbuster Buff** | You know your classics, respect. |
    | **C** | **Cousin Status** | You're invited to the cookout, but don't touch the music. |
    | **D** | **Director’s Cut** | You need to spend a weekend on Tubi or Netflix. |
    | **F** | **First Time?** | "Bye, Felicia!" |
    """)

    st.write("---")
    
    # LEADERBOARD SECTION
    st.write("### 🏆 Hall of Fame")
    name = st.text_input("Enter your name to save your score:")
    if st.button("Save My Score"):
        if name:
            st.session_state.leaderboard.append({"Name": name, "Score": f"{score}/{total}", "Grade": grade})
            st.success("Score saved!")

    if st.session_state.leaderboard:
        df = pd.DataFrame(st.session_state.leaderboard)
        st.table(df)

    if st.button("🔄 Restart Quiz"):
        st.session_state.quiz_step = 0
        st.session_state.score = 0
        st.session_state.hint = ""
        st.rerun()
