import streamlit as st
from utils import load_css, run_watson_granite
import random

# Page config
st.set_page_config(
    page_title="EduNexus 2.0 - Mental Health Support",
    page_icon="🧠",
    layout="wide"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Mental Health Support 🧠</h1>", unsafe_allow_html=True)

# Description
st.markdown(
    """<div class='card'>
        <p>Your mental well-being matters. This space is designed to provide support, 
        encourage relaxation, and help manage academic stress.</p>
    </div>""",
    unsafe_allow_html=True
)

# Daily Inspiration
inspirational_quotes = [
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "You are stronger than you know. - Unknown",
    "Every day is a fresh start. - Unknown",
    "Your mental health is a priority. - Unknown",
    "Small steps lead to big changes. - Unknown"
]

st.markdown(
    f"""<div class='card'>
        <h3>Today's Inspiration</h3>
        <p style='text-align: center; font-style: italic;'>{random.choice(inspirational_quotes)}</p>
    </div>""",
    unsafe_allow_html=True
)

# Mood Tracker
st.markdown("<h2 class='sub-title'>Mood Check-in</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    mood = st.select_slider(
        "How are you feeling today?",
        options=["😔 Very Low", "😟 Low", "😐 Neutral", "🙂 Good", "😊 Very Good"],
        value="😐 Neutral"
    )
    
    stress_level = st.slider(
        "Current Stress Level",
        0, 10, 5,
        help="0 = No stress, 10 = Extremely stressed"
    )

with col2:
    if st.button("Get Personalized Support"):
        prompt = f"""Based on the user's current mood ({mood}) and stress level ({stress_level}/10), 
        provide a supportive and encouraging message along with 2-3 practical coping strategies. 
        Keep the tone warm and empathetic."""
        
        response = run_watson_granite(prompt)
        st.markdown(f"""<div class='response-area'>{response}</div>""", unsafe_allow_html=True)

# Relaxation Techniques
st.markdown("<h2 class='sub-title'>Relaxation Techniques</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<div class='card'>
            <h3>🧘‍♀️ Breathing Exercise</h3>
            <p>Try the 4-7-8 breathing technique:</p>
            <ol>
                <li>Inhale for 4 seconds</li>
                <li>Hold for 7 seconds</li>
                <li>Exhale for 8 seconds</li>
            </ol>
        </div>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """<div class='card'>
            <h3>🎵 Music Therapy</h3>
            <p>Listen to calming music or nature sounds while studying.</p>
            <p>Recommended: Classical music, ambient sounds, or white noise.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """<div class='card'>
            <h3>✍️ Journaling</h3>
            <p>Write down your thoughts and feelings. What's on your mind today?</p>
        </div>""",
        unsafe_allow_html=True
    )

# Support Resources
st.markdown("<h2 class='sub-title'>Need More Support?</h2>", unsafe_allow_html=True)

st.markdown(
    """<div class='card'>
        <h3>📞 Emergency Contacts</h3>
        <ul>
            <li>National Crisis Hotline: 988</li>
            <li>Student Counseling Services: [Your School's Number]</li>
            <li>Crisis Text Line: Text HOME to 741741</li>
        </ul>
        <p class='info-text'>Remember: It's okay to ask for help. You're not alone.</p>
    </div>""",
    unsafe_allow_html=True
)

# Guided Support
support_topics = [
    "Managing Academic Stress",
    "Dealing with Test Anxiety",
    "Balancing Study and Life",
    "Improving Sleep Habits",
    "Building Self-Confidence"
]

st.markdown("<h2 class='sub-title'>Guided Support</h2>", unsafe_allow_html=True)

selected_topic = st.selectbox("Choose a topic you'd like guidance with:", support_topics)

if st.button("Get Guidance"):
    prompt = f"""Provide practical advice and strategies for: {selected_topic}
    Include:
    1. Understanding the challenge
    2. Immediate coping strategies
    3. Long-term solutions
    4. When to seek additional help
    Keep the tone supportive and encouraging."""
    
    response = run_watson_granite(prompt)
    st.markdown(f"""<div class='response-area'>{response}</div>""", unsafe_allow_html=True)