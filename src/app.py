import os
import random
import streamlit as st

from tone_mapper import get_prosody
from tts_engine import synthesize_to_mp3
VOICE_OPTIONS = {
    "UK Male (Ryan)": "en-GB-RyanNeural",
    "UK Female (Sonia)": "en-GB-SoniaNeural",
    "US Male (Guy)": "en-US-GuyNeural",
    "US Female (Jenny)": "en-US-JennyNeural",
}
TONE_STYLE = {
    "horror": {
        "adjectives": ["cold", "unnatural", "breathless", "shadowed", "hollow"],
        "verbs": ["stalked", "whispered", "crept", "scratched", "echoed"],
        "ending_feel": "something followed even after it ended"
    },
    "romantic": {
        "adjectives": ["warm", "soft", "familiar", "bright", "gentle"],
        "verbs": ["glowed", "lingered", "sparked", "drifted", "returned"],
        "ending_feel": "hope settled in like light through curtains"
    },
    "comedy": {
        "adjectives": ["ridiculous", "chaotic", "awkward", "dramatic", "unhelpful"],
        "verbs": ["tripped", "panicked", "blurted", "spilled", "improvised"],
        "ending_feel": "everyone survived, somehow"
    },
    "sad": {
        "adjectives": ["quiet", "heavy", "distant", "pale", "tired"],
        "verbs": ["faded", "broke", "waited", "remembered", "left"],
        "ending_feel": "the memory stayed, but the pain softened"
    },
    "angry": {
        "adjectives": ["sharp", "raw", "burning", "restless", "stormy"],
        "verbs": ["snapped", "challenged", "refused", "confronted", "pushed"],
        "ending_feel": "the truth was spoken out loud"
    },
    "calm": {
        "adjectives": ["still", "clear", "simple", "peaceful", "steady"],
        "verbs": ["breathed", "settled", "flowed", "rested", "waited"],
        "ending_feel": "everything felt a little lighter"
    },
}

GENRE_SETTINGS = {
    "Fantasy": ["an ancient library of spells", "a forest that remembers names", "a floating city of lanterns", "a ruined temple under moonlight"],
    "Romance": ["a small hotel with warm lights", "a rainy café", "a train ride at sunset", "a quiet street festival"],
    "Sci-Fi": ["a space station corridor", "a neon city controlled by algorithms", "a research lab after midnight", "a ship drifting beyond known maps"],
    "Horror": ["an abandoned hotel hallway", "a locked basement room", "a village that avoids the same door", "a mirror that reflects too slowly"],
    "Mystery": ["a hotel lobby with one too many keys", "a museum after closing time", "a townhouse with hidden passages", "a letter with no return address"],
    "Comedy": ["a hotel breakfast buffet warzone", "an office meeting gone wrong", "a family dinner full of secrets", "a date that collapses in five minutes"],
}

GENRE_CONFLICTS = {
    "Fantasy": ["a curse begins to wake", "a stolen relic changes hands", "a prophecy points to the wrong person", "a gate opens when it shouldn’t"],
    "Romance": ["a misunderstanding grows legs", "a secret is revealed too soon", "two people keep missing their moment", "the past returns at the worst time"],
    "Sci-Fi": ["an AI makes an emotional decision", "time glitches for a few minutes", "the system rewrites the rules", "a message arrives from tomorrow"],
    "Horror": ["a sound repeats at the same hour", "someone knocks from inside the wall", "a shadow appears without a body", "the building learns your name"],
    "Mystery": ["an alibi doesn’t match the clock", "a clue is planted on purpose", "the victim isn’t who they claimed", "someone lies with perfect calm"],
    "Comedy": ["a tiny lie becomes a full-time job", "a simple plan explodes instantly", "the 'expert' is totally useless", "everything goes wrong in public"],
}

GENRE_TWISTS = {
    "Fantasy": ["the villain is protecting something", "the magic answers incorrectly", "the hero is the missing piece", "the map changes while you watch"],
    "Romance": ["the stranger is someone from years ago", "the letter wasn’t meant for you—but it was", "the 'goodbye' becomes a beginning", "the truth makes everything clearer"],
    "Sci-Fi": ["the clone remembers another life", "the simulation breaks for a second", "gravity shifts and reality follows", "the AI asks for forgiveness"],
    "Horror": ["the voice is your own", "the mirror smiles back", "you were never alone", "the exit leads back inside"],
    "Mystery": ["the clue points to the detective", "the 'missing' person planned it", "the obvious suspect is innocent", "the answer was in plain sight"],
    "Comedy": ["the solution makes it worse", "everyone saw it happen", "you accidentally win", "the truth is funnier than the lie"],
}


def pick_style(tone: str):
    t = (tone or "calm").lower().strip()
    return TONE_STYLE.get(t, TONE_STYLE["calm"])


def build_story(prompt: str, genre: str, tone: str, target_words: int) -> str:
    """
    Builds a story with NEW paragraphs (no repetition loops).
    More words => more unique scenes.
    """
    style = pick_style(tone)
    adj = style["adjectives"]
    vb = style["verbs"]

    setting = random.choice(GENRE_SETTINGS.get(genre, ["a strange place"]))
    conflict = random.choice(GENRE_CONFLICTS.get(genre, ["something unexpected happens"]))
    twist = random.choice(GENRE_TWISTS.get(genre, ["everything changes"]))

    protagonist = random.choice(["I", "We", "They"])
    detail = random.choice([
        "a key with a number scratched into it",
        "a note folded into a perfect square",
        "a bruise-shaped shadow on the ceiling",
        "a scent of coffee and rain",
        "a suitcase that feels too heavy",
        "a phone that keeps lighting up with no notifications",
    ])

    prompt_line = prompt.strip()
    if not prompt_line:
        prompt_line = "something unusual happens"

    paragraphs = []
    paragraphs.append(
        f"{protagonist} {random.choice(vb)} into {setting}, and the air felt {random.choice(adj)}. "
        f"It started with {detail}."
    )
    paragraphs.append(
        f"{prompt_line.capitalize()}—and at first it seemed simple enough to ignore. "
        f"But the place reacted, like it had been waiting."
    )
    paragraphs.append(
        f"By the time we noticed the pattern, it was too late. {conflict.capitalize()}. "
        f"Every hallway, every conversation, every glance felt {random.choice(adj)}."
    )
    paragraphs.append(
        f"{protagonist} tried to act normal, but normal didn’t fit anymore. "
        f"Outside, the world kept moving. Inside, something {random.choice(vb)} closer."
    )
    paragraphs.append(
        f"Then the twist arrived: {twist}. "
        f"In that moment, the meaning of {detail} changed completely."
    )
    extra_scene_bank = [
        f"A stranger offered help, but their smile didn’t reach their eyes.",
        f"The lights flickered, and for a second the room looked different—older.",
        f"Someone said a name that nobody had spoken aloud.",
        f"A choice appeared: tell the truth, or keep the peace and pay for it later.",
        f"The silence was so deep it felt like an answer.",
        f"A door opened that should have been locked.",
        f"A laugh escaped at the worst possible time, and it cracked the tension in two.",
        f"Time felt uneven, like the minutes were skipping stones across a lake.",
    ]

    while len(" ".join(paragraphs).split()) < target_words - 80:
        paragraphs.append(random.choice(extra_scene_bank))
    paragraphs.append(
        f"In the end, {protagonist.lower()} didn’t get everything we wanted. "
        f"But {style['ending_feel']}. And that was enough."
    )

    return "\n\n".join(paragraphs)


def generate_story(prompt: str, genre: str, tone: str, word_count: int):
    title = f"{genre} Tale ({tone})"
    story_only = build_story(prompt, genre, tone, word_count)

    display_text = f"""
Title: {title}

Prompt: {prompt}

Story:
{story_only}
""".strip()

    return display_text, story_only


def ensure_outputs_folder() -> str:
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
    os.makedirs(out_dir, exist_ok=True)
    return out_dir
st.set_page_config(page_title="Creative Writing Buddy (Text + Tone TTS)", layout="centered")
st.title("Creative Writing Buddy 🎭🔊")
st.write("Generate creative text and hear it narrated with tone and storyteller voice control.")

prompt = st.text_area("Your prompt", placeholder="e.g., a mysterious door appears in my bedroom...")

col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("Genre", ["Fantasy", "Romance", "Sci-Fi", "Horror", "Mystery", "Comedy"])
with col2:
    tone = st.selectbox("Tone", ["horror", "romantic", "comedy", "sad", "angry", "calm"])

voice_label = st.selectbox("Storyteller voice", list(VOICE_OPTIONS.keys()))
voice_id = VOICE_OPTIONS[voice_label]

word_count = st.slider("Approx. story length (words)", min_value=150, max_value=1000, value=350, step=50)

if st.button("Generate text + audio"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    display_text, narration_text = generate_story(prompt, genre, tone, word_count)

    st.subheader("Generated Text")
    st.write(display_text)

    prosody = get_prosody(tone)
    out_dir = ensure_outputs_folder()
    mp3_path = os.path.join(out_dir, "output.mp3")

    with st.spinner("Generating audio narration..."):
        synthesize_to_mp3(
            text=narration_text,
            output_file=mp3_path,
            voice=voice_id,
            rate=prosody["rate"],
            pitch=prosody["pitch"],
            volume=prosody["volume"],
        )

    st.subheader("Audio Narration")
    st.audio(mp3_path, format="audio/mp3")
    st.success("Done! Try changing the prompt, genre, tone, length, and voice.")
