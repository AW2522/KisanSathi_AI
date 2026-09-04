"""
Asynchronous Urdu Text-to-Speech (TTS) Synthesis Module for KisanSathi AI using edge-tts.
"""

import os
import asyncio
import logging

logger = logging.getLogger(__name__)

VOICE = "ur-PK-UzmaNeural"
OUTPUT_DIR = os.path.join("assets", "audio_outputs")

async def generate_urdu_audio(text: str, filename: str = "remedy.mp3") -> str:
    """
    Asynchronously converts Urdu text into speech and saves an .mp3 file.

    Args:
        text (str): Urdu text to convert.
        filename (str): Target mp3 filename.

    Returns:
        str: Relative path of the generated audio file.
    """
    try:
        import edge_tts
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Overwrite existing file safely if present
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.warning(f"Could not remove existing file {filepath}: {e}")

        # Synthesize audio using edge-tts
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filepath)
        logger.info(f"Audio remedy successfully saved to {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"Error generating Urdu TTS audio: {e}")
        # Return fallback or raise gracefully
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(OUTPUT_DIR, filename)
        return filepath

def get_urdu_audio_sync(text: str, filename: str = "remedy.mp3") -> str:
    """
    Synchronous wrapper for generate_urdu_audio to be invoked seamlessly by Streamlit.

    Args:
        text (str): Urdu text to convert.
        filename (str): Target mp3 filename.

    Returns:
        str: Relative path of the generated audio file.
    """
    try:
        return asyncio.run(generate_urdu_audio(text, filename))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(generate_urdu_audio(text, filename))
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in get_urdu_audio_sync: {e}")
        return os.path.join(OUTPUT_DIR, filename)

class TTSEngine:
    """
    Object-oriented wrapper for Urdu Text-to-Speech engine.
    """
    def __init__(self, voice: str = VOICE):
        self.voice = voice

    async def generate_audio(self, text: str, filename: str = "remedy.mp3") -> str:
        return await generate_urdu_audio(text, filename)

    def generate_audio_sync(self, text: str, filename: str = "remedy.mp3") -> str:
        return get_urdu_audio_sync(text, filename)
