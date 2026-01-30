
TONE_TO_PROSODY = {
    "horror": {
        "rate": "-20%",
        "pitch": "-25Hz",
        "volume": "-10%"
    },
    "romantic": {
        "rate": "-10%",
        "pitch": "+10Hz",
        "volume": "+0%"
    },
    "comedy": {
        "rate": "+15%",
        "pitch": "+15Hz",
        "volume": "+10%"
    },
    "sad": {
        "rate": "-15%",
        "pitch": "-10Hz",
        "volume": "-15%"
    },
    "angry": {
        "rate": "+10%",
        "pitch": "+5Hz",
        "volume": "+15%"
    },
    "calm": {
        "rate": "-5%",
        "pitch": "-5Hz",
        "volume": "-5%"
    }
}

def get_prosody(tone: str) -> dict:
    """
    Returns prosody settings (rate, pitch, volume)
    for a given tone. Falls back to neutral if unknown.
    """
    if not tone:
        return {"rate": "0%", "pitch": "0Hz", "volume": "0%"}

    tone = tone.lower().strip()
    return TONE_TO_PROSODY.get(
        tone,
        {"rate": "0%", "pitch": "0Hz", "volume": "0%"}
    )
