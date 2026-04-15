import streamlit as st
import pandas as pd
import altair as alt
import os
from core.emotion_analyzer import EmotionAnalyzer
from core.voice_synthesizer import generate_audio
from core.config import EMOTION_MAP

st.set_page_config(page_title="Empathy Engine", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #070709 !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,30,255,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,210,180,0.08) 0%, transparent 60%),
        #070709 !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

section[data-testid="stSidebar"] { display: none; }

.block-container {
    max-width: 960px !important;
    padding: 3rem 2rem 4rem !important;
    margin: 0 auto;
}

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.25em;
    color: #00d2b4;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero h1 {
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 30%, #a78bfa 70%, #00d2b4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.75rem;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #5a5a72;
    letter-spacing: 0.05em;
}

/* ── DIVIDER ── */
.rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.3), rgba(0,210,180,0.3), transparent);
    margin: 2rem 0;
}

/* ── INPUT CARD ── */
.input-wrap {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}
.input-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(99,30,255,0.06), transparent 50%);
    pointer-events: none;
}
.input-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: #5a5a72;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.stTextArea textarea {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    padding: 1rem 1.2rem !important;
    resize: none !important;
    transition: border-color 0.2s;
}
.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.08) !important;
}
.stTextArea textarea::placeholder { color: #3a3a52 !important; }
.stTextArea label { display: none !important; }

/* ── BUTTON ── */
            
/* ── SELECTBOX ── */
.stSelectbox div[data-baseweb="select"] {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    transition: border-color 0.2s;
}
.stSelectbox div[data-baseweb="select"]:hover {
    border-color: rgba(167,139,250,0.5) !important;
}
.stSelectbox span[data-baseweb="icon"] { color: #5a5a72 !important; }
div[data-testid="stSelectbox"] { margin-bottom: 0.5rem; }
            
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #6318ff 0%, #4f0fd4 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    text-transform: uppercase !important;
    position: relative;
    overflow: hidden;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── RESULTS SECTION ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: #5a5a72;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* ── EMOTION BADGE ── */
.emotion-hero-card {
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
}
.emotion-badge-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 0.4rem;
}
.emotion-badge-name {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1;
}
.emotion-badge-conf {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    margin-top: 0.5rem;
    opacity: 0.6;
}

/* ── PROSODY PILLS ── */
.prosody-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
}
.prosody-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
}
.prosody-pill-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    color: #4a4a62;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.prosody-pill-val {
    font-family: 'DM Mono', monospace;
    font-size: 17px;
    font-weight: 500;
    color: #e0e0f0;
}

/* ── CHART SECTION ── */
.chart-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.4rem 1.5rem 1rem;
}

/* ── AUDIO CARD ── */
.audio-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.stAudio {
    border-radius: 10px !important;
    margin-top: 0.75rem !important;
    width: 100% !important;
}
audio {
    filter: invert(0.9) hue-rotate(200deg);
    border-radius: 10px;
    width: 100%;
}

/* ── WAVEFORM ANIMATION ── */
.waveform {
    display: flex;
    align-items: center;
    gap: 3px;
    height: 32px;
    margin: 0.75rem 0;
}
.waveform span {
    display: inline-block;
    width: 3px;
    border-radius: 3px;
    animation: wave 1.2s ease-in-out infinite;
}
.waveform span:nth-child(1)  { animation-delay: 0.0s; height: 40%; }
.waveform span:nth-child(2)  { animation-delay: 0.1s; height: 70%; }
.waveform span:nth-child(3)  { animation-delay: 0.2s; height: 100%; }
.waveform span:nth-child(4)  { animation-delay: 0.15s; height: 60%; }
.waveform span:nth-child(5)  { animation-delay: 0.25s; height: 85%; }
.waveform span:nth-child(6)  { animation-delay: 0.05s; height: 50%; }
.waveform span:nth-child(7)  { animation-delay: 0.3s; height: 75%; }
.waveform span:nth-child(8)  { animation-delay: 0.1s; height: 45%; }
.waveform span:nth-child(9)  { animation-delay: 0.2s; height: 90%; }
.waveform span:nth-child(10) { animation-delay: 0s; height: 55%; }
.waveform span:nth-child(11) { animation-delay: 0.35s; height: 65%; }
.waveform span:nth-child(12) { animation-delay: 0.15s; height: 80%; }

@keyframes wave {
    0%, 100% { transform: scaleY(0.4); opacity: 0.5; }
    50%       { transform: scaleY(1);   opacity: 1; }
}

/* ── METRICS OVERRIDE ── */
[data-testid="metric-container"] { display: none !important; }

/* ── SPINNER ── */
[data-testid="stSpinner"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    color: #5a5a72 !important;
    letter-spacing: 0.1em !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
    background: rgba(255,60,60,0.08) !important;
    border: 1px solid rgba(255,60,60,0.2) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
[data-testid="stWarning"] {
    background: rgba(255,180,0,0.08) !important;
    border: 1px solid rgba(255,180,0,0.2) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.06) !important; margin: 2rem 0 !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def get_analyzer():
    analyzer = EmotionAnalyzer()
    analyzer.load_model()
    return analyzer

analyzer = get_analyzer()

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Neural Prosody Engine</div>
    <h1>The Empathy Engine</h1>
    <div class="hero-sub">[ NLP · Emotion Detection · Adaptive TTS · Dynamic Prosody Modulation ]</div>
</div>
<div class="rule"></div>
""", unsafe_allow_html=True)

# ── INPUT ──
st.markdown('<div class="input-wrap"><div class="input-label">▸ Input Source Text</div>', unsafe_allow_html=True)

# Dictionary of curated emotional sample sentences
SAMPLE_PROMPTS = {
    "✍️ Type your own custom text below or select sample examples from dropdown menu": "",
    "😠 [ Anger ] This is completely unacceptable!": "This is completely unacceptable! I explicitly told them not to do this and they completely ignored me!",
    "😔 [ Sadness ] We have to scrap the project...": "We unfortunately have to scrap the entire project after months of hard work. It's really disappointing.",
    "😨 [ Fear ] I don't think we should be here...": "I am terrified of what might happen if the storm hits while we are still on the road.",
    "😲 [ Surprise ] They approved the proposal?!": "Wait, the client actually approved the proposal without a single revision? I'm completely shocked!",
    "🤢 [ Disgust ] That is absolutely disgusting...": "That is absolutely revolting. I can't even stand to look at it, it makes me sick.",
    "😐 [ Neutral ] The function takes a string...": "The function takes a string as an input and returns a dictionary of the analyzed results.",
    "😄 [ Joy ] The build passed perfectly!": "The build passed and it deployed perfectly on the very first try! Best day ever."
}

# Dropdown for selecting a sample
selected_prompt_key = st.selectbox(
    "Select a sample prompt",
    options=list(SAMPLE_PROMPTS.keys()),
    label_visibility="collapsed"
)

# Text area automatically populates with the selected sample, but remains fully editable
user_input = st.text_area(
    "Source Text",
    value=SAMPLE_PROMPTS[selected_prompt_key],
    placeholder="Enter text to analyze and synthesize...",
    height=110,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
run = st.button("⚡  Run Emotion & Voice Synthesis", type="primary")

if run:
    if not user_input.strip():
        st.warning("⚠  Input field is empty. Please enter source text.")
    else:
        with st.spinner("Running NLP pipeline..."):
            analysis = analyzer.analyze(user_input)

        if not analysis["success"]:
            st.error("Engine Error: Emotion analysis failed.")
        else:
            dom_label = analysis["dominant"]["label"]
            dom_score = analysis["dominant"]["score"]
            map_data  = EMOTION_MAP[dom_label]
            color     = map_data["color"]

            st.markdown("<div class='rule'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>▸ Analysis Output</div>", unsafe_allow_html=True)

            # ── TOP ROW: Emotion Card + Prosody Pills ──
            left, right = st.columns([1, 1.6], gap="medium")

            with left:
                glow_color = color + "22"
                st.markdown(f"""
                <div class="emotion-hero-card" style="background: linear-gradient(135deg, {color}18, {color}06); border-color: {color}44;">
                    <div class="emotion-badge-label">Dominant Emotion</div>
                    <div class="emotion-badge-name" style="color:{color}">
                        {map_data['emoji']}&nbsp; {dom_label.upper()}
                    </div>
                    <div class="emotion-badge-conf">Confidence — {dom_score:.1%}</div>
                    <div class="waveform" style="margin-top:1rem">
                        {''.join(f'<span style="background:{color}"></span>' for _ in range(12))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with right:
                st.markdown(f"""
                <div style="padding:0.2rem 0">
                    <div class="section-label">▸ Prosody Modulation</div>
                    <div class="prosody-grid">
                        <div class="prosody-pill">
                            <div class="prosody-pill-label">Rate</div>
                            <div class="prosody-pill-val" style="color:{color}">{map_data['rate']}</div>
                        </div>
                        <div class="prosody-pill">
                            <div class="prosody-pill-label">Pitch</div>
                            <div class="prosody-pill-val" style="color:{color}">{map_data['pitch']}</div>
                        </div>
                        <div class="prosody-pill">
                            <div class="prosody-pill-label">Volume</div>
                            <div class="prosody-pill-val" style="color:{color}">{map_data['volume']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

            # ── BOTTOM ROW: Chart + Audio ──
            chart_col, audio_col = st.columns([1.6, 1], gap="medium")

            with chart_col:
                st.markdown('<div class="chart-card"><div class="section-label">▸ Full Emotional Spectrum</div>', unsafe_allow_html=True)

                df = pd.DataFrame(analysis["all_scores"])
                df["label"] = df["label"].str.capitalize()

                chart = (
                    alt.Chart(df)
                    .mark_bar(cornerRadiusEnd=5, height=18)
                    .encode(
                        x=alt.X("score:Q", title=None,
                                scale=alt.Scale(domain=[0, 1]),
                                axis=alt.Axis(format="%", labelColor="#3a3a52",
                                              tickColor="#3a3a52", domainColor="#3a3a52",
                                              labelFont="DM Mono", labelFontSize=10)),
                        y=alt.Y("label:N", title=None, sort="-x",
                                axis=alt.Axis(labelColor="#9090b0", labelFont="Syne",
                                              labelFontSize=12, labelFontWeight=600,
                                              tickColor="transparent", domainColor="transparent")),
                        color=alt.condition(
                            alt.datum.label == dom_label.capitalize(),
                            alt.value(color),
                            alt.value("#1e1e2e")
                        ),
                        tooltip=[
                            alt.Tooltip("label:N", title="Emotion"),
                            alt.Tooltip("score:Q", format=".2%", title="Confidence")
                        ]
                    )
                    .properties(height=220, background="transparent")
                    .configure_view(strokeWidth=0)
                    .configure_axis(grid=False)
                )

                st.altair_chart(chart, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with audio_col:
                st.markdown('<div class="audio-card"><div class="section-label">▸ Synthesized Voice</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin: 0.5rem 0 1rem">
                    <div style="font-family:'DM Mono',monospace;font-size:11px;color:#5a5a72;margin-bottom:6px">Voice Profile</div>
                    <div style="font-size:13px;font-weight:700;color:#e0e0f0;letter-spacing:0.05em">NeerjaNeural · en-IN</div>
                    <div style="font-size:11px;font-family:'DM Mono',monospace;color:{color};margin-top:4px">
                        {dom_label.upper()} · {dom_score:.0%} conf.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.spinner("Rendering audio..."):
                    audio_result = generate_audio(user_input, dom_label)
                    if audio_result["success"]:
                        st.audio(audio_result["path"], format="audio/mp3")
                        os.remove(audio_result["path"])
                    else:
                        st.error("Audio generation failed.")

                st.markdown("</div>", unsafe_allow_html=True)

            # ── FOOTER ──
            st.markdown(f"""
            <div style="margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.05);
                        display:flex;align-items:center;justify-content:space-between">
                <div style="font-family:'DM Mono',monospace;font-size:10px;color:#2e2e42;letter-spacing:0.15em">
                    EMPATHY ENGINE · NEURAL PROSODY
                </div>
                <div style="font-family:'DM Mono',monospace;font-size:10px;color:#2e2e42;letter-spacing:0.1em">
                    EDGE — {color.upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)