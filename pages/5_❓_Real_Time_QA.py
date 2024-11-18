import streamlit as st
from utils import load_css, run_watson_granite, show_error, show_success

# Page config
st.set_page_config(
    page_title="EduNexus 2.0 - Real-Time Q&A",
    page_icon="❓",
    layout="wide"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Real-Time Q&A Support ❓</h1>", unsafe_allow_html=True)

# Description
st.markdown(
    """<div class='card'>
        <p>Get instant answers to your academic questions! Our AI-powered system can help you with 
        any subject or topic. Try some example questions or ask your own.</p>
    </div>""",
    unsafe_allow_html=True
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Example questions
st.markdown("<h2 class='sub-title'>Example Questions</h2>", unsafe_allow_html=True)

example_questions = [
    "Explain the concept of photosynthesis in simple terms.",
    "What are the key differences between Python and Java?",
    "How do I solve quadratic equations?",
    "What were the main causes of World War II?",
    "Explain the law of conservation of energy."
]

# Main interface
col1, col2 = st.columns([3, 1])

with col1:
    # Chat input and button in the same column
    user_question = st.text_area("Your Question", height=100,
        placeholder="Type your question here or select from example questions...")
    
    # Get Answer button right below the text area
    if st.button("🤔 Get Answer", use_container_width=True):
        if user_question:
            with st.spinner("Thinking..."):
                chat_context = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history[-3:]])
                prompt = f"""Context of previous questions (if any):
                {chat_context}
                
                Current question: {user_question}
                
                Please provide a clear, detailed, and educational answer. Include examples where appropriate."""
                
                response = run_watson_granite(prompt)
                st.session_state.chat_history.append((user_question, response))
                show_success("Response generated!")
                st.rerun()
        else:
            show_error("Please enter a question first!")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p><strong>Try these examples:</strong></p>", unsafe_allow_html=True)
    for question in example_questions:
        if st.button(f"📝 {question}", key=f"example_{question}", use_container_width=True):
            with st.spinner("Thinking..."):
                prompt = f"""Please provide a clear, detailed, and educational answer to this question:
                {question}
                
                Include examples where appropriate and make it easy to understand."""
                
                response = run_watson_granite(prompt)
                st.session_state.chat_history.append((question, response))
                show_success("Response generated!")
                st.rerun()

# Display chat history
if st.session_state.chat_history:
    st.markdown("<h2 class='sub-title'>Conversation History</h2>", unsafe_allow_html=True)
    
    for question, answer in reversed(st.session_state.chat_history):
        st.markdown(
            f"""<div class='card'>
                <h4>Question:</h4>
                <p>{question}</p>
                <h4>Answer:</h4>
                <div class='response-area'>{answer}</div>
            </div>""",
            unsafe_allow_html=True
        )

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🧹 Clear History"):
            st.session_state.chat_history = []
            show_success("History cleared!")
            st.rerun()

# Tips Section
st.markdown("<h2 class='sub-title'>Tips for Asking Questions</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<div class='card'>
            <h3>🎯 Be Specific</h3>
            <p>The more specific your question, the better the answer you'll receive.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """<div class='card'>
            <h3>📚 Provide Context</h3>
            <p>Include relevant background information or context for more accurate answers.</p>
        </div>""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """<div class='card'>
            <h3>🔍 Follow Up</h3>
            <p>Don't hesitate to ask follow-up questions for better understanding.</p>
        </div>""",
        unsafe_allow_html=True
    )

# Footer
st.markdown(
    """<div style='text-align: center; margin-top: 3rem; padding: 1rem; background-color: #262730; border-radius: 0.5rem;'>
        <p>Learning is a journey of questions and discoveries!</p>
        <p class='info-text'>Keep asking, keep learning! ❓</p>
    </div>""",
    unsafe_allow_html=True
)