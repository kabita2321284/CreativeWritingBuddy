
This project is a multimodal creative writing chatbot that generates a short story and narrates it aloud using Text-to-Speech (TTS).  
The narration style changes based on the selected tone (speed, pitch, volume) and the user can also choose the storyteller voice.
- Story generation (genre + prompt)
- Tone-based narration control (rate, pitch, volume)
- Storyteller voice selection
- Streamlit web interface
- Outputs MP3 narration
- src/ : Python source code
- outputs/ : Generated MP3 files
- report/ : Project report (add your report here)
```bash
pip install -r requirements.txt
python src/app.py
