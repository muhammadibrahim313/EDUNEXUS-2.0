import streamlit as st
from utils import load_css, run_watson_granite

# Page config
st.set_page_config(
    page_title="EduNexus 2.0 - Study Planner",
    page_icon="📅",
    layout="wide"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Interactive Study Planner 📅</h1>", unsafe_allow_html=True)

# Description
st.markdown(
    """<div class='card'>
        <p>Create your personalized study plan by filling in the details below. Our AI will generate 
        a comprehensive schedule tailored to your needs and goals.</p>
    </div>""",
    unsafe_allow_html=True
)

# Input Form
with st.form("study_plan_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.text_input("Subject/Topic", placeholder="e.g., Mathematics, Physics, Programming")
        duration = st.selectbox("Study Duration", 
            ["1 week", "2 weeks", "1 month", "2 months", "3 months", "6 months"])
        difficulty_level = st.select_slider("Current Knowledge Level",
            options=["Beginner", "Elementary", "Intermediate", "Advanced", "Expert"])

    with col2:
        goal = st.text_area("Learning Goals", 
            placeholder="What do you want to achieve? Be specific about your objectives.")
        study_hours = st.number_input("Available Hours per Week", min_value=1, max_value=40, value=10)
        preferred_time = st.multiselect("Preferred Study Time",
            ["Early Morning", "Late Morning", "Afternoon", "Evening", "Night"],
            default=["Afternoon"])

    submit_button = st.form_submit_button("Generate Study Plan")

# Handle form submission
if submit_button:
    if not subject or not goal:
        st.error("Please fill in both subject and learning goals!")
    else:
        with st.spinner("Generating your personalized study plan..."):
            prompt = f"""Create a detailed study plan based on the following parameters:
            Subject: {subject}
            Duration: {duration}
            Knowledge Level: {difficulty_level}
            Goals: {goal}
            Available Hours: {study_hours} hours per week
            Preferred Study Time: {', '.join(preferred_time)}

            Please provide a structured plan including:
            1. Weekly breakdown of topics
            2. Daily study schedule
            3. Learning milestones
            4. Recommended resources
            5. Progress tracking metrics
            """

            response = run_watson_granite(prompt)

            st.markdown("<h2 class='sub-title'>Your Personalized Study Plan</h2>", unsafe_allow_html=True)
            st.markdown(f"""<div class='response-area'>{response}</div>""", unsafe_allow_html=True)

            # Download button for the study plan
            st.download_button(
                label="Download Study Plan",
                data=response,
                file_name=f"study_plan_{subject.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )

# Tips Section
st.markdown("<h2 class='sub-title'>Study Tips</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<div class='card'>
            <h3>🎯 Set Clear Goals</h3>
            <p>Break down your main goal into smaller, achievable milestones.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """<div class='card'>
            <h3>⏰ Time Management</h3>
            <p>Use the Pomodoro Technique: 25 minutes of focused study followed by a 5-minute break.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """<div class='card'>
            <h3>📊 Track Progress</h3>
            <p>Regularly review and adjust your study plan based on your progress.</p>
        </div>""",
        unsafe_allow_html=True
    )