import asyncio
import edge_tts
import tempfile
from core.config import EMOTION_MAP, TTS_VOICE

async def _generate_async(text, emotion):
    params = EMOTION_MAP.get(emotion, EMOTION_MAP["neutral"])
    
    # We now pass rate, pitch, AND volume to the synthesis engine
    communicate = edge_tts.Communicate(
        text, 
        TTS_VOICE, 
        rate=params["rate"], 
        pitch=params["pitch"],
        volume=params["volume"] 
    )
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        
    await communicate.save(temp_path)
    return temp_path

def generate_audio(text, emotion):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        file_path = loop.run_until_complete(_generate_async(text, emotion))
        return {"success": True, "path": file_path}
    except Exception as e:
        return {"success": False, "error": str(e)}