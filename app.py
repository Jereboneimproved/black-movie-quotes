import streamlit as st
import google.generativeai as genai
import random

# --- CLOUD CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")

# --- APP SETUP ---
st.set_page_config(page_title="The Culture Quote Quiz", page_icon="🎬")

# --- MOVIE DATA (Your full list) ---
quiz_data = [
    {"quote": "Surely you can't be serious. / I am serious... and don't call me Shirley.", "options": ["Airplane!", "Coming to America", "Friday"], "answer": "Airplane!", "actor": "Kareem Abdul-Jabbar"},
    {"quote": "The royal penis is clean, your Highness.", "options": ["Coming to America", "Boomerang", "New Jack City"], "answer": "Coming to America", "actor": "The Bathers"},
    {"quote": "Don’t nobody go in the bathroom for about 35, 45 minutes.", "options": ["Friday", "Do the Right Thing", "Training Day"], "answer": "Friday", "actor": "Bernie Mac"},
    {"quote": "Bye, Felicia.", "options": ["Friday", "New Jack City", "Boomerang"], "answer": "Friday", "actor": "Ice Cube"},
    {"quote": "King Kong ain't got shit on me!", "options": ["Training Day", "Black Panther", "The Woman King"], "answer": "Training Day", "actor": "Denzel Washington"},
    {"quote": "I am your wife! I am the greatest good you are ever gonna get!", "options": ["The Incredibles", "Princess and the Frog", "The Wiz"], "answer": "The Incredibles", "actor": "Samuel L. Jackson (Frozone's Wife)"},
    {"quote": "Wakanda Forever!", "options": ["Black Panther", "Origin", "The Book of Clarence"], "answer": "Black Panther", "actor": "Chadwick Boseman"},
    {"quote": "Heritage isn't just what was left for us; it’s what we build for them.", "options": ["Horizon: New World", "The Woman King", "Fade to Black"], "answer": "Horizon: New World", "actor": "Future Diaspora"},
    {"quote": "Love should've brought your ass home last night.", "options": ["Boomerang", "Friday", "Coming to America"], "answer": "Boomerang", "actor": "Grace Jones"},
    {"quote": "Always do the right thing.", "options": ["Do the Right Thing", "New Jack City", "The Fresh Prince"], "answer": "Do the Right Thing", "actor": "Da Mayor"},
    {"quote": "I’m not a businessman; I’m a business, man.", "options": ["Fade to Black", "Training Day", "The Fast and the Furious"], "answer": "Fade to Black", "actor": "Jay-Z"},
    {"quote": "The ancestors didn't just survive; they dreamed of us.", "options": ["Origin", "The Book of Clarence", "The Woman King"], "answer": "Origin", "actor": "Aunjanue Ellis-Taylor"}
]

# --- SESSION STATE ---
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'hint' not in st.session_state:
    st.session_state.hint = ""

def next_question(selected):
    if selected == quiz_data[st.session_state.quiz_step]['answer']:
        st.session_state.score += 1
    st.session_state.quiz_step += 1
    st.session_state.hint
