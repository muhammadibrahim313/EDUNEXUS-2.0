import streamlit as st
from utils import load_css, run_watson_granite

# Page config
st.set_page_config(
    page_title="EduNexus 2.0 - Multi-Language Support",
    page_icon="🌍",
    layout="wide"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Multi-Language Support 🌍</h1>", unsafe_allow_html=True)

# Description
st.markdown(
    """<div class='card'>
        <p>Break language barriers in your learning journey! Ask questions in your preferred language 
        and get responses translated back. Perfect for bilingual and multilingual students.</p>
    </div>""",
    unsafe_allow_html=True
)

# Language Selection
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Hindi": "hi",
    "Arabic": "ar",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru"
}

# Language Settings
col1, col2 = st.columns(2)
with col1:
    input_language = st.selectbox("Select Your Input Language", list(languages.keys()))
with col2:
    output_language = st.selectbox("Select Your Output Language", list(languages.keys()), index=0)

# Question Input
user_input = st.text_area(
    f"Enter your question in {input_language}",
    height=100,
    placeholder=f"Type your question in {input_language}..."
)

# Translation and Response
if st.button("Get Answer"):
    if user_input:
        with st.spinner("Processing your question..."):
            # First, translate to English if not already in English
            if input_language != "English":
                translation_prompt = f"""Translate the following text from {input_language} to English:
                
                Text: {user_input}
                
                Provide only the English translation without any explanations."""
                
                english_query = run_watson_granite(translation_prompt)
            else:
                english_query = user_input
            
            # Get the answer in English
            answer_prompt = f"""Question: {english_query}
            Please provide a clear and detailed answer."""
            
            english_answer = run_watson_granite(answer_prompt)
            
            # Translate answer if needed
            if output_language != "English":
                final_translation_prompt = f"""Translate the following text from English to {output_language}:
                
                Text: {english_answer}
                
                Provide only the {output_language} translation without any explanations."""
                
                final_answer = run_watson_granite(final_translation_prompt)
            else:
                final_answer = english_answer
            
            # Display results
            st.markdown("<h2 class='sub-title'>Your Answer</h2>", unsafe_allow_html=True)
            
            # Show original question
            st.markdown(
                f"""<div class='card'>
                    <h4>Original Question ({input_language}):</h4>
                    <p>{user_input}</p>
                </div>""",
                unsafe_allow_html=True
            )
            
            # Show answer
            st.markdown(
                f"""<div class='response-area'>
                    <h4>Answer in {output_language}:</h4>
                    <p>{final_answer}</p>
                </div>""",
                unsafe_allow_html=True
            )

# Language Learning Tools
st.markdown("<h2 class='sub-title'>Language Learning Tools</h2>", unsafe_allow_html=True)

# Vocabulary Builder
st.markdown("<h3>Vocabulary Builder</h3>", unsafe_allow_html=True)

topic = st.selectbox(
    "Select a topic to learn vocabulary:",
    ["Academic", "Science", "Technology", "Mathematics", "Literature", "History"]
)

if st.button("Generate Vocabulary List"):
    vocab_prompt = f"""Create a vocabulary list for {topic} with 10 important terms.
    For each term, provide:
    1. The word in {output_language}
    2. Its English translation
    3. A brief definition in {output_language}
    4. An example sentence in {output_language}"""
    
    vocab_response = run_watson_granite(vocab_prompt)
    st.markdown(f"""<div class='response-area'>{vocab_response}</div>""", unsafe_allow_html=True)

# Practice Exercises
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<div class='card'>
            <h3>🎯 Translation Practice</h3>
            <p>Practice translating common academic phrases between languages.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """<div class='card'>
            <h3>📝 Writing Helper</h3>
            <p>Get help with writing academic content in different languages.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """<div class='card'>
            <h3>🗣️ Pronunciation Guide</h3>
            <p>Learn how to pronounce technical terms correctly.</p>
        </div>""",
        unsafe_allow_html=True
    )

# Tips Section
st.markdown("<h2 class='sub-title'>Language Learning Tips</h2>", unsafe_allow_html=True)

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown(
        """<div class='card'>
            <h3>Study Tips</h3>
            <ul>
                <li>Practice regularly with native content</li>
                <li>Use flashcards for vocabulary</li>
                <li>Join language exchange groups</li>
                <li>Watch educational videos in target language</li>
            </ul>
        </div>""",
        unsafe_allow_html=True
    )

with tips_col2:
    st.markdown(
        """<div class='card'>
            <h3>Common Mistakes to Avoid</h3>
            <ul>
                <li>Relying too much on direct translation</li>
                <li>Ignoring pronunciation practice</li>
                <li>Not practicing regularly</li>
                <li>Focusing only on vocabulary</li>
            </ul>
        </div>""",
        unsafe_allow_html=True
    )