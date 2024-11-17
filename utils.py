import streamlit as st
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes, DecodingMethods
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv('.streamlit/secrets.toml')

def init_watsonx():
    """Initialize WatsonX credentials and return model inference object"""
    try:
        api_key = os.getenv('WATSONX_APIKEY')
        project_id = os.getenv('WATSONX_PROJECT_ID')
        url = os.getenv('WATSONX_URL')

        if not all([api_key, project_id, url]):
            raise ValueError("Missing required WatsonX credentials")

        gen_params = {
            GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
            GenParams.TEMPERATURE: 0.7,
            GenParams.MIN_NEW_TOKENS: 10,
            GenParams.MAX_NEW_TOKENS: 2048
        }

        return ModelInference(
            model_id="ibm/granite-3-8b-instruct",
            params=gen_params,
            credentials=Credentials(
                api_key=api_key,
                url=url
            ),
            project_id=project_id
        )
    except Exception as e:
        st.error(f"Error initializing WatsonX: {str(e)}")
        return None

def run_watson_granite(prompt, system_prompt=""):
    """Run WatsonX model with error handling"""
    try:
        model_inference = init_watsonx()
        if not model_inference:
            return "Error: Could not initialize WatsonX model"

        complete_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = model_inference.generate(complete_prompt)
        
        if not response or 'results' not in response:
            raise ValueError("Invalid response from WatsonX")

        generated_texts = [item.get('generated_text', '') for item in response['results']]
        return generated_texts[0] if generated_texts else "No response generated"

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if 'model_inference' in locals():
            del model_inference

# UI Components
def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #FF4B4B;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 500;
        color: #FAFAFA;
        margin: 1rem 0;
    }
    
    .card {
        background-color: #262730;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .response-area {
        background-color: #1E1E1E;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #FF4B4B;
    }
    
    .info-text {
        color: #B2B2B2;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    .button-primary {
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    
    .button-primary:hover {
        background-color: #FF6B6B;
    }
    </style>
    """

def show_error(message):
    st.error(f"🚨 {message}")

def show_success(message):
    st.success(f"✅ {message}")

def show_info(message):
    st.info(f"ℹ️ {message}")

def show_warning(message):
    st.warning(f"⚠️ {message}")