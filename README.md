# 🎙️ The Empathy Engine

**Giving AI a Human Voice through Dynamic Prosody Modulation.**

![UI Showcase](https://via.placeholder.com/1000x500.png?text=UI+Screenshot+Goes+Here) ## 📖 Vision & Context
In the world of AI-driven interactions, standard Text-to-Speech (TTS) systems are highly functional but emotionally robotic. They lack the prosody, emotional range, and subtle vocal cues necessary to build true user rapport. 

**The Empathy Engine** bridges this "uncanny valley." It is a dynamic vocal modulation service that analyzes the emotional subtext of an input string and programmatically alters the rate, pitch, and amplitude of a neural TTS engine to achieve genuine emotional resonance. 

## ✨ Key Features
* **Granular Emotion Detection:** Bypasses basic positive/negative sentiment analysis by utilizing a pre-trained RoBERTa NLP model to classify text into 7 nuanced emotional states (Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral).
* **Dynamic Prosody Mapping:** Programmatically alters the `Rate`, `Pitch`, and `Volume` of the synthesized speech based on a scientifically tuned emotional matrix.
* **Identity Anchoring:** Implements strict pitch-variance constraints to prevent "Formant Shifting," ensuring the AI maintains a consistent biometric identity across all emotional states.
* **Neural Normalization Bypass:** Utilizes extreme amplitude overrides to successfully bypass the internal audio compressors inherent in modern neural TTS engines.
* **Modern SaaS Interface:** A sleek, fully functional frontend built with Streamlit, featuring custom CSS, glassmorphism UI elements, and interactive data visualization via Altair.

---

## ⚙️ Environment Setup & Installation

This project is built using Python 3.8+ and utilizes Hugging Face Transformers and Microsoft Edge-TTS.

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd Empathy_engine
```
2. Environment Configuration
Ensure your project structure matches the following architecture:
Empathy_engine/
├── .env
├── .gitignore
├── app.py
├── requirements.txt
└── core/
    ├── __init__.py
    ├── config.py
    ├── emotion_analyzer.py
    └── voice_synthesizer.py
