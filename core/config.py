TTS_VOICE = "en-IN-NeerjaNeural" 


EMOTION_MAP = {
    # UPBEAT: Faster rate, slight pitch bump, but balanced volume so it's not shouting.
    "joy": {"rate": "+20%", "pitch": "+6Hz", "volume": "+40%", "emoji": "😄", "color": "#4CAF50"},
    
    # HEAVY: Drastically slower and much quieter to simulate a lack of energy.
    "sadness": {"rate": "-16%", "pitch": "-8Hz", "volume": "-25%", "emoji": "😔", "color": "#2196F3"},
    
    # AGGRESSIVE: Fast and loud, lower pitch for authority/threat.
    "anger": {"rate": "+28%", "pitch": "-3Hz", "volume": "+75%", "emoji": "😠", "color": "#F44336"},
    
    # TENSE: Higher pitch, quiet volume (like a tense whisper), slightly faster.
    "fear": {"rate": "+10%", "pitch": "-5Hz", "volume": "-60%", "emoji": "😨", "color": "#9C27B0"},
    
    # SHOCKED: Fast, high pitch, slight volume bump.
    "surprise": {"rate": "+20%", "pitch": "+8Hz", "volume": "+8%", "emoji": "😲", "color": "#FF9800"},
    
    # REJECTION: Slower, lower pitch, slightly louder to emphasize the "yuck" factor.
    "disgust": {"rate": "-10%", "pitch": "-6Hz", "volume": "+10%", "emoji": "🤢", "color": "#795548"},
    
    # BASELINE
    "neutral": {"rate": "+0%", "pitch": "+0Hz", "volume": "+0%", "emoji": "😐", "color": "#9E9E9E"},
}