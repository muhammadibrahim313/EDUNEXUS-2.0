import streamlit as st
from utils import load_css, run_watson_granite, show_error, show_success

# Page config
st.set_page_config(page_title="Personalized Learning Assistant", page_icon="🎓", layout="wide")

# Load CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Personalized Learning Assistant 🎓</h1>", unsafe_allow_html=True)

# Initialize session state for conversation history
if 'learning_history' not in st.session_state:
    st.session_state.learning_history = []

# Default questions/templates
default_questions = {
    "Create a learning plan": "Create a detailed learning plan for [TOPIC] including objectives, timeline, and resources.",
    "Explain a concept": "Explain [CONCEPT] in simple terms with examples.",
    "Study techniques": "What are the most effective study techniques for [SUBJECT]?",
    "Find resources": "Suggest learning resources for [TOPIC] including books, courses, and online materials."
}

# Sidebar with default questions
st.sidebar.markdown("<h2 class='sub-title'>Quick Templates</h2>", unsafe_allow_html=True)
selected_template = st.sidebar.selectbox(
    "Choose a template:",
    list(default_questions.keys())
)

if selected_template:
    template_text = default_questions[selected_template]
    st.sidebar.markdown(f"**Template:**\n\n{template_text}")

# Main chat interface
st.markdown(
    """<div class='card'>
        <h3>How can I help you learn today?</h3>
        <p class='info-text'>Ask me anything about your learning journey, and I'll provide personalized guidance.</p>
    </div>""",
    unsafe_allow_html=True
)

# User input
user_input = st.text_area("Type your question or use a template:", height=100)

# Buttons
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🧹 Clear History"):
        st.session_state.learning_history = []
        show_success("Conversation history cleared!")
        st.rerun()

with col2:
    if st.button("🚀 Get Help"):
        if user_input:
            try:
                # System prompt for learning assistant
                system_prompt = """You are an expert educational advisor and learning assistant. 
                Your role is to provide detailed, personalized learning guidance and support.
                Focus on breaking down complex topics, suggesting practical learning strategies,
                and creating structured learning plans. Be encouraging and supportive while
                maintaining academic rigor."""
                
                response = run_watson_granite(user_input, system_prompt)
                
                if response and not response.startswith("Error"):
                    st.session_state.learning_history.append(
                        {"question": user_input, "answer": response}
                    )
                    show_success("Response generated!")
                else:
                    show_error(f"Failed to get response: {response}")
                
            except Exception as e:
                show_error(f"An error occurred: {str(e)}")
        else:
            show_error("Please enter your question first!")

# Display conversation history
if st.session_state.learning_history:
    st.markdown("<h2 class='sub-title'>Learning Journey</h2>", unsafe_allow_html=True)
    
    for idx, interaction in enumerate(reversed(st.session_state.learning_history)):
        st.markdown(
            f"""<div class='card'>
                <p><strong>Question:</strong></p>
                <p>{interaction['question']}</p>
                <div class='response-area'>
                    <p><strong>Response:</strong></p>
                    <p>{interaction['answer']}</p>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

# Tips and Resources
with st.expander("📚 Learning Tips & Resources"):
    st.markdown(
        """
        ### Effective Learning Strategies
        * **Active Recall**: Test yourself frequently
        * **Spaced Repetition**: Review material at increasing intervals
        * **Pomodoro Technique**: Study in focused 25-minute sessions
        * **Mind Mapping**: Create visual connections between concepts
        * **Teaching Others**: Explain concepts to reinforce learning
        
        ### Recommended Learning Platforms
        * Coursera
        * edX
        * Khan Academy
        * MIT OpenCourseWare
        * Codecademy (for programming)
        """
    )

# Footer
st.markdown(
    """<div style='text-align: center; margin-top: 3rem; padding: 1rem; background-color: #262730; border-radius: 0.5rem;'>
        <p>Remember: The journey of learning is just as important as the destination.</p>
        <p class='info-text'>Need help? Don't hesitate to ask!</p>
    </div>""",
    unsafe_allow_html=True
)