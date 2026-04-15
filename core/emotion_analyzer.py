import os
import streamlit as st
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

class EmotionAnalyzer:
    def __init__(self):
        self.classifier = None

    def load_model(self):
        """Loads the Hugging Face model gracefully with secure token auth."""
        try:
            if self.classifier is None:
                # 1. Securely fetch the token (checks Streamlit secrets first, then local .env)
                hf_token = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))
                
                if not hf_token:
                    print("Warning: No HF_TOKEN found. Proceeding without authentication.")
                
                # 2. Initialize the pipeline with the token
                self.classifier = pipeline(
                    "text-classification", 
                    model="j-hartmann/emotion-english-distilroberta-base", 
                    top_k=None,
                    token=hf_token  
                )
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def analyze(self, text):
        """Analyzes text and returns all emotion probabilities."""
        try:
            if not self.classifier:
                self.load_model()
            
            results = self.classifier(text)[0]
            dominant_emotion = max(results, key=lambda x: x['score'])
            
            return {
                "success": True,
                "dominant": dominant_emotion,
                "all_scores": results
            }
        except Exception as e:
            return {"success": False, "error": str(e)}