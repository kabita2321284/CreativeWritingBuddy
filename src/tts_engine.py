
import asyncio
import edge_tts

DEFAULT_VOICE = "en-GB-RyanNeural"

async def _synthesize_async(text: str, output_file: str, voice: str, rate: str, pitch: str, volume: str):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume
    )
    await communicate.save(output_file)

def synthesize_to_mp3(
    text: str,
    output_file: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "0%",
    pitch: str = "0Hz",
    volume: str = "0%"
):
    """
    Synthesize plain text to an MP3 file using Edge TTS with selectable voice and prosody controls.
    """
    asyncio.run(_synthesize_async(text, output_file, voice, rate, pitch, volume))
