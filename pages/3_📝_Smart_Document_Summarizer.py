import streamlit as st
from utils import load_css, run_watson_granite, show_error, show_success, show_info
import re

# Page config
st.set_page_config(page_title="Smart Document Summarizer", page_icon="📝", layout="wide")

# Load CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Smart Document Summarizer 📝</h1>", unsafe_allow_html=True)

# Initialize session state
if 'summaries' not in st.session_state:
    st.session_state.summaries = []

# Sidebar options
st.sidebar.markdown("<h2 class='sub-title'>Summary Options</h2>", unsafe_allow_html=True)

summary_type = st.sidebar.selectbox(
    "Summary Type",
    ["Concise", "Detailed", "Bullet Points", "Academic", "Simple Language"]
)

summary_length = st.sidebar.slider(
    "Summary Length (% of original)",
    min_value=10,
    max_value=50,
    value=30,
    step=5
)

# Main interface
st.markdown(
    """<div class='card'>
        <h3>Document Summarization</h3>
        <p class='info-text'>Paste your document text below for a clear, structured summary.</p>
    </div>""",
    unsafe_allow_html=True
)

# Document input
document_text = st.text_area("Paste your document text here:", height=200)

# Word count
if document_text:
    word_count = len(re.findall(r'\w+', document_text))
    st.markdown(f"Word count: {word_count}")

# Buttons
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🧹 Clear History"):
        st.session_state.summaries = []
        show_success("History cleared!")
        st.rerun()

with col2:
    if st.button("🚀 Generate Summary"):
        if document_text:
            try:
                # System prompt for summarization
                system_prompt = f"""You are an expert document summarizer.
                Create a {summary_type.lower()} summary that is approximately {summary_length}% 
                of the original length. Focus on key points and maintain coherence.
                Format the summary with:
                1. Main Points
                2. Key Details
                3. Important Conclusions
                4. Key Terms (if any)
                
                Make the summary clear and well-structured."""
                
                response = run_watson_granite(document_text, system_prompt)
                
                if not response.startswith("Error"):
                    st.session_state.summaries.append({
                        "original": document_text,
                        "summary": response,
                        "type": summary_type,
                        "length": summary_length
                    })
                    show_success("Summary generated!")
                else:
                    show_error(f"Summarization failed: {response}")
                    
            except Exception as e:
                show_error(f"An error occurred: {str(e)}")
        else:
            show_error("Please enter the document text first!")

# Display summaries
if st.session_state.summaries:
    st.markdown("<h2 class='sub-title'>Generated Summaries</h2>", unsafe_allow_html=True)
    
    for idx, summary in enumerate(reversed(st.session_state.summaries)):
        with st.expander(f"Summary {len(st.session_state.summaries) - idx} - {summary['type']}"):
            st.markdown(
                f"""<div class='card'>
                    <p><strong>Original Text:</strong></p>
                    <div style='max-height: 200px; overflow-y: auto; padding: 1rem; 
                              background-color: #1E1E1E; border-radius: 0.5rem;'>
                        {summary['original'][:500]}{'...' if len(summary['original']) > 500 else ''}
                    </div>
                    <div class='response-area'>
                        <p><strong>Summary ({summary['length']}% length):</strong></p>
                        {summary['summary']}
                    </div>
                </div>""",
                unsafe_allow_html=True
            )

# ... existing code ...

# Tips for better summaries
with st.expander("📚 Tips for Better Summaries"):
    st.markdown("""
    ### Tips for Better Results:
    1. **Clean your text**: Remove any unnecessary formatting or special characters
    2. **Break into sections**: If summarizing a long document, consider breaking it into smaller sections
    3. **Choose the right summary type**:
        - *Concise*: For quick overview
        - *Detailed*: For comprehensive understanding
        - *Bullet Points*: For easy scanning
        - *Academic*: For formal documents
        - *Simple Language*: For general audience
    4. **Adjust length**: Use the slider to find the optimal summary length for your needs
    """)