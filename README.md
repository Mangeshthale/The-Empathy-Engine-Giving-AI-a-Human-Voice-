# 🎙️ The Empathy Engine

**Giving AI a Human Voice through Dynamic Prosody Modulation.**

🚀 **[Try the Live Demo Here!](https://empathyengine.streamlit.app/)** 🚀

## 📖 Vision & Context

In the world of AI-driven interactions, standard Text-to-Speech (TTS) systems are highly functional but emotionally robotic. They lack the prosody, emotional range, and subtle vocal cues necessary to build true user rapport. 

**The Empathy Engine** bridges this "uncanny valley." It is a dynamic vocal modulation service that analyzes the emotional subtext of an input string and programmatically alters the rate, pitch, and amplitude of a neural TTS engine to achieve genuine emotional resonance.

## ✨ Key Features

- **Granular Emotion Detection:** Bypasses basic positive/negative sentiment analysis by utilizing a pre-trained RoBERTa NLP model to classify text into 7 nuanced emotional states (Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral).
- **Dynamic Prosody Mapping:** Programmatically alters the `Rate`, `Pitch`, and `Volume` of the synthesized speech based on a scientifically tuned emotional matrix.
- **Identity Anchoring:** Implements strict pitch-variance constraints to prevent "Formant Shifting," ensuring the AI maintains a consistent biometric identity across all emotional states.
- **Neural Normalization Bypass:** Utilizes extreme amplitude overrides to successfully bypass the internal audio compressors inherent in modern neural TTS engines.
- **Modern SaaS Interface:** A sleek, fully functional frontend built with Streamlit, featuring custom CSS, glassmorphism UI elements, and interactive data visualization via Altair.

---

## ⚙️ Environment Setup & Installation

This project is built using Python 3.10+ and utilizes Hugging Face Transformers and Microsoft Edge-TTS.

### 1. Clone the Repository

```bash
git clone [https://github.com/Mangeshthale/The-Empathy-Engine-Giving-AI-a-Human-Voice-](https://github.com/Mangeshthale/The-Empathy-Engine-Giving-AI-a-Human-Voice-)
cd Empathy_engine
```

### 2. Environment Configuration

Ensure your project structure matches the following architecture:

```text
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
```

### 3. Install Dependencies

Create a virtual environment (recommended) and install the required packages:

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. API Keys & Secrets

Create a `.env` file in the root directory to store your Hugging Face token securely. This prevents API rate-limiting during the NLP inference stage.
```bash
.env
HF_TOKEN=your_huggingface_token_here
```

### 5. Run the Engine

Launch the Streamlit application:

```bash
streamlit run app.py
```

> Note: The first time you run the application, it will download the Hugging Face distilroberta model (~300MB). Subsequent runs will load instantly from the local cache.

## 🧠 System Architecture & Design Choices

### The Modular Approach

Instead of a monolithic script, the engine is divided into distinct, scalable micro-components:

- `emotion_analyzer.py`: The **"Brain."** Handles the heavy lifting of loading and inferencing the Hugging Face transformer.
- `voice_synthesizer.py`: The **"Vocal Cords."** Manages async network calls to the TTS API.
- `config.py`: The **"DNA."** Centralizes all prosody tuning logic and voice selection.

### Emotion-to-Voice Logic (Prosody Mapping)

Mapping human emotion to numerical API parameters is a complex challenge. The logic in `core/config.py` was specifically engineered to solve two major roadblocks in Generative Voice AI:

#### 1. Solving "Identity Loss" (Formant Shifting)

When aggressively modifying the pitch parameter in neural TTS engines, the AI alters the perceived size of the simulated vocal tract. This causes the voice to sound like a completely different person (e.g., a +20Hz shift sounds like a child, a -20Hz shift sounds like a giant)

**The Solution:** The `EMOTION_MAP` heavily restricts pitch variance to a safe +8Hz / -8Hz band. This acts as an "Identity Anchor," ensuring the speaker remains recognizable across all emotions. Emotional weight is instead conveyed via aggressive Rate and Volume manipulation.

#### 2. Bypassing Neural Gain Control

Modern neural voices (like `en-IN-NeerjaNeural`) are trained on professionally mastered audio and feature internal compressors that normalize volume to prevent audio peaking.

**The Solution:** To force the AI to genuinely whisper in "Fear" or shout in "Anger," the engine utilizes extreme volume parameters (e.g., +75% for Anger, -60% for Fear). These extreme values successfully override the engine's Automatic Gain Control.

### Sample Matrix Examples

- **Sadness:** Heavy, slow delivery (Rate: -16%), lowered vocal cords (Pitch: -8Hz), and heavily compressed amplitude (Volume: -25%).
- **Anger:** Fast, aggressive delivery (Rate: +28%), commanding lower pitch (Pitch: -3Hz), and absolute maximum amplitude (Volume: +75%).

### Voice Localization

The engine utilizes `en-IN-NeerjaNeural`, a high-fidelity Indian-English female voice. This was a deliberate design choice to provide a localized, highly relatable, and deeply empathetic UX for users within the targeted demographic, proving that the engine can adapt to global accents while maintaining emotional integrity.
