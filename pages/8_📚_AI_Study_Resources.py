import streamlit as st
from utils import load_css, run_watson_granite
import json

# Page config
st.set_page_config(
    page_title="EduNexus 2.0 - AI Study Resources",
    page_icon="📚",
    layout="wide"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>AI-Generated Study Resources 📚</h1>", unsafe_allow_html=True)

# Description
st.markdown(
    """<div class='card'>
        <p>Generate customized study materials tailored to your needs. Create practice exams, 
        flashcards, and revision materials instantly with AI assistance.</p>
    </div>""",
    unsafe_allow_html=True
)

# Resource Type Selection
st.markdown("<h2 class='sub-title'>Choose Resource Type</h2>", unsafe_allow_html=True)

resource_type = st.radio(
    "What type of study resource would you like to generate?",
    ["Practice Exam", "Flashcards", "Study Notes", "Mind Map", "Quiz"]
)

# Common Input Fields
col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Subject/Topic", placeholder="e.g., Biology, Physics, History")
    difficulty = st.select_slider(
        "Difficulty Level",
        options=["Beginner", "Elementary", "Intermediate", "Advanced", "Expert"]
    )

with col2:
    subtopics = st.text_area(
        "Specific Topics to Cover",
        placeholder="Enter specific topics, separated by commas"
    )
    education_level = st.selectbox(
        "Education Level",
        ["High School", "Undergraduate", "Graduate", "Professional"]
    )

# Resource-specific inputs and generation
if resource_type == "Practice Exam":
    exam_cols1, exam_cols2 = st.columns(2)
    
    with exam_cols1:
        question_count = st.number_input("Number of Questions", 5, 50, 10)
        time_limit = st.number_input("Suggested Time Limit (minutes)", 15, 180, 60)
    
    with exam_cols2:
        question_types = st.multiselect(
            "Question Types",
            ["Multiple Choice", "True/False", "Short Answer", "Essay", "Problem Solving"],
            ["Multiple Choice", "Short Answer"]
        )

elif resource_type == "Flashcards":
    card_count = st.number_input("Number of Flashcards", 5, 50, 20)
    include_examples = st.checkbox("Include examples with each card", True)

elif resource_type == "Study Notes":
    format_style = st.selectbox(
        "Note Format",
        ["Outline", "Detailed Notes", "Summary", "Cornell Notes"]
    )
    include_diagrams = st.checkbox("Include diagram descriptions", True)

elif resource_type == "Mind Map":
    central_topic = st.text_input("Central Topic", placeholder="Main concept to map")
    depth_level = st.slider("Depth Level", 1, 4, 2)

elif resource_type == "Quiz":
    quiz_cols1, quiz_cols2 = st.columns(2)
    
    with quiz_cols1:
        quiz_questions = st.number_input("Number of Questions", 5, 30, 10)
        include_explanations = st.checkbox("Include Explanations", True)
    
    with quiz_cols2:
        quiz_type = st.selectbox(
            "Quiz Type",
            ["Multiple Choice", "Fill in the Blanks", "Mixed"]
        )

# Generate Button
if st.button("Generate Study Resource"):
    if not subject or not subtopics:
        st.error("Please fill in both subject and specific topics!")
    else:
        with st.spinner("Generating your study resource..."):
            # Prepare base prompt
            base_prompt = f"""Create a {resource_type} for {subject} at {education_level} level.
            Difficulty: {difficulty}
            Topics: {subtopics}
            """
            
            # Add resource-specific parameters to prompt
            if resource_type == "Practice Exam":
                prompt = base_prompt + f"""
                Generate {question_count} questions including {', '.join(question_types)}.
                Time Limit: {time_limit} minutes
                
                Format:
                1. Instructions and time limit
                2. Questions with clear numbering
                3. Answer key with explanations
                """
            
            elif resource_type == "Flashcards":
                prompt = base_prompt + f"""
                Create {card_count} flashcards with:
                1. Term/Question side
                2. Definition/Answer side
                {' 3. Example usage' if include_examples else ''}
                
                Format each card clearly with "Front:" and "Back:"
                """
            
            elif resource_type == "Study Notes":
                prompt = base_prompt + f"""
                Create {format_style} style notes with:
                1. Main concepts
                2. Key points and definitions
                3. Examples and explanations
                {' 4. Relevant diagram descriptions' if include_diagrams else ''}
                """
            
            elif resource_type == "Mind Map":
                prompt = base_prompt + f"""
                Create a text-based mind map for "{central_topic}" with:
                1. Central concept
                2. Main branches (Level 1)
                3. Sub-branches up to Level {depth_level}
                4. Key connections and relationships
                
                Use indentation and symbols to show hierarchy.
                """
            
            elif resource_type == "Quiz":
                prompt = base_prompt + f"""
                Create a {quiz_type} quiz with {quiz_questions} questions.
                {' Include detailed explanations for each answer.' if include_explanations else ''}
                
                Format:
                1. Questions clearly numbered
                2. Answer options (if multiple choice)
                3. Correct answers
                {' 4. Explanations' if include_explanations else ''}
                """

            # Generate content
            response = run_watson_granite(prompt)
            
            # Display generated content
            st.markdown("<h2 class='sub-title'>Your Generated Resource</h2>", unsafe_allow_html=True)
            st.markdown(f"""<div class='response-area'>{response}</div>""", unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                label="Download Resource",
                data=response,
                file_name=f"{subject.lower().replace(' ', '_')}_{resource_type.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )

# Tips Section
st.markdown("<h2 class='sub-title'>Study Tips</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<div class='card'>
            <h3>📝 Practice Exams</h3>
            <p>Take in exam-like conditions for the best preparation.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """<div class='card'>
            <h3>🔄 Flashcard Usage</h3>
            <p>Review cards regularly and shuffle them to improve recall.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """<div class='card'>
            <h3>📊 Track Progress</h3>
            <p>Monitor your understanding with regular self-assessment.</p>
        </div>""",
        unsafe_allow_html=True
    )

# Resource Library
st.markdown("<h2 class='sub-title'>Recently Generated Resources</h2>", unsafe_allow_html=True)

# Initialize session state for resource history
if 'resource_history' not in st.session_state:
    st.session_state.resource_history = []

# Display recent resources
if st.session_state.resource_history:
    for resource in st.session_state.resource_history[-5:]:  # Show last 5 resources
        st.markdown(
            f"""<div class='card'>
                <h4>{resource['type']}: {resource['subject']}</h4>
                <p>Created: {resource['date']}</p>
            </div>""",
            unsafe_allow_html=True
        )
else:
    st.info("No resources generated yet. Create your first resource above!")