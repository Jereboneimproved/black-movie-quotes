import streamlit as st
import google.generativeai as genai
import random
import pandas as pd
import time

# --- CLOUD CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")

# --- APP SETUP ---
st.set_page_config(page_title="The Culture Quote Quiz", page_icon="🎬")

# Initialize Session States
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'hint' not in st.session_state:
    st.session_state.hint = ""
if 'current_options' not in st.session_state:
    st.session_state.current_options = []

# --- MOVIE DATA ---
quiz_data = [
    {"quote": "Surely you can't be serious. / I am serious... and don't call me Shirley.", "options": ["Airplane!", "Coming to America", "Friday", "The Wiz", "Do the Right Thing"], "answer": "Airplane!", "actor": "Kareem Abdul-Jabbar"},
    {"quote": "The royal penis is clean, your Highness.", "options": ["Coming to America", "Boomerang", "New Jack City", "Harlem Nights", "The Color Purple"], "answer": "Coming to America", "actor": "The Bathers"},
    {"quote": "Don’t nobody go in the bathroom for about 35, 45 minutes.", "options": ["Friday", "Do the Right Thing", "Training Day", "Life", "Belly"], "answer": "Friday", "actor": "Bernie Mac"},
    {"quote": "Bye, Felicia.", "options": ["Friday", "New Jack City", "Boomerang", "Barbershop", "Set It Off"], "answer": "Friday", "actor": "Ice Cube"},
    {"quote": "King Kong ain't got shit on me!", "options": ["Training Day", "Black Panther", "The Woman King", "American Gangster", "Malcolm X"], "answer": "Training Day", "actor": "Denzel Washington"},
    {"quote": "I am your wife! I am the greatest good you are ever gonna get!", "options": ["The Incredibles", "Princess and the Frog", "The Wiz", "Soul", "Spider-Verse"], "answer": "The Incredibles", "actor": "Honey Best"},
    {"quote": "Wakanda Forever!", "options": ["Black Panther", "Origin", "The Book of Clarence", "The Woman King", "Tenet"], "answer": "Black Panther", "actor": "Chadwick Boseman"},
    {"quote": "Love should've brought your ass home last night.", "options": ["Boomerang", "Friday", "Coming to America", "Waitress", "Waiting to Exhale"], "answer": "Boomerang", "actor": "Grace Jones"},
    {"quote": "Always do the right thing.", "options": ["Do the Right Thing", "New Jack City", "The Fresh Prince", "He Got Game", "Jungle Fever"], "answer": "Do the Right Thing", "actor": "Da Mayor"},
    {"quote": "I’m not a businessman; I’m a business, man.", "options": ["Fade to Black", "Training Day", "The Fast and the Furious", "Paid in Full", "State Property"], "answer": "Fade to Black", "actor": "Jay-Z"},
    {"quote": "The ancestors didn't just survive; they dreamed of us.", "options": ["Origin", "The Book of Clarence", "The Woman King", "12 Years a Slave", "Harriet"], "answer": "Origin", "actor": "Aunjanue Ellis-Taylor"}
]

st.title("🎬 The Culture Quote Quiz")

# --- HALFWAY CHECKPOINT ---
if st.session_state.quiz_step == 6 and 'halfway_seen' not in st.session_state:
    st.header("⏸️ Intermission: The Oracle Speaks")
    with st.spinner("Analyzing your performance..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            score_context = "killing it" if st.session_state.score >= 4 else "struggling"
            prompt = f"Write a funny 1-sentence commentary for someone with a {st.session_state.score}/5 score on a Black cinema quiz. Use 'cookout' vibes. They are {score_context}."
            response = model.generate_content(prompt)
            msg = response.text
        except:
            msg = "The ancestors are watching... let's see if you can pull this off."
    st.info(msg)
    if st.button("Continue to the Second Half ➡️"):
        st.session_state.halfway_seen = True
        st.rerun()

# --- QUIZ INTERFACE ---
elif st.session_state.quiz_step < len(quiz_data):
    current = quiz_data[st.session_state.quiz_step]
    if not st.session_state.current_options:
        shuffled = current['options'].copy()
        random.shuffle(shuffled)
        st.session_state.current_options = shuffled

    st.subheader(f"Question {st.session_state.quiz_step + 1} of {len(quiz_data)}")
    timer_placeholder = st.empty()
    st.info(f"\"{current['quote']}\"")
    
    if st.button("💡 Need a Hint?"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Give a funny 1-sentence hint for the quote '{current['quote']}'. Don't name the movie."
            response = model.generate_content(prompt)
            st.session_state.hint = response.text
        except:
            st.session_state.hint = "Think back to the last family reunion."
            
    if st.session_state.hint:
        st.write(f"*{st.session_state.hint}*")

    choice = st.radio("Choose the correct movie:", st.session_state.current_options, key=f"q_{st.session_state.quiz_step}")
    
    if st.button("Submit Answer 🎯"):
        is_correct = choice == current['answer']
        lesson = ""
        if not is_correct:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                p = f"Explain why '{current['answer']}' is iconic and the line '{current['quote']}' matters. 1 sentence, cookout vibes."
                response = model.generate_content(p)
                lesson = response.text
            except:
                lesson = "This is a culture essential!"
        
        if is_correct: st.session_state.score += 1
        
        st.session_state.history.append({
            "Movie": current['answer'],
            "Result": "✅" if is_correct else "❌",
            "Culture Lesson": lesson if not is_correct else "You know your stuff!"
        })
        st.session_state.quiz_step += 1
        st.session_state.hint = ""
        st.session_state.current_options = []
        st.rerun()

    # TIMER LOGIC
    for seconds in range(20, -1, -1):
        if seconds > 5:
            timer_placeholder.markdown(f"### ⏳ Time Remaining: **{seconds}s**")
        else:
            alarm = "🚨" if seconds % 2 == 0 else "⚠️"
            timer_placeholder.markdown(f"### :red[{alarm} HURRY UP: **{seconds}s** {alarm}]")
        time.sleep(1)
        if seconds == 0:
            st.session_state.history.append({"Movie": current['answer'], "Result": "❌ (Timed Out)", "Culture Lesson": "Too slow! Rewatch this classic."})
            st.session_state.quiz_step += 1
            st.session_state.current_options = []
            st.rerun()

# --- FINAL RESULTS ---
else:
    total = len(quiz_data)
    score = st.session_state.score
    percent = (score / total) * 100
    
    if percent >= 90: grade, desc = "A", "Ancestor Approved"
    elif percent >= 80: grade, desc = "B", "Blockbuster Buff"
    elif percent >= 70: grade, desc = "C", "Cousin Status"
    elif percent >= 60: grade, desc = "D", "Director’s Cut"
    else: grade, desc = "F", "First Time?"

    st.header(f"🏁 Final Grade: {grade}")
    st.markdown(f"### **{desc}**")
    
    # CLICKABLE REVIEW
    with st.expander("➡️ CLICK HERE to Review & Learn from the Culture", icon="📖"):
        st.table(pd.DataFrame(st.session_state.history))

    # SHARE BUTTON
    share_text = f"I just got a Grade {grade} ({desc}) on the Culture Quote Quiz! My score: {score}/{total}. Can you beat me? 🎬🔥"
    st.text_area("Copy/Paste to your Group Chat:", value=share_text, height=70)

    # GRADING TABLE
    st.markdown("""
    | Grade | Meaning | Vibe |
    | :--- | :--- | :--- |
    | **A** | **Ancestor Approved** | Keeper of the culture. |
    | **B** | **Blockbuster Buff** | Respect. |
    | **C** | **Cousin Status** | Don't touch the music. |
    | **D** | **Director’s Cut** | Weekend on Tubi. |
    | **F** | **First Time?** | "Bye, Felicia!" |
    """)

    st.write("---")
    st.write("### 🏆 Hall of Fame")
    name = st.text_input("Enter your name:")
