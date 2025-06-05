# Streamlit Meeting Transcription Tool

This app lets you upload an MP3 or WAV file, transcribe it using OpenAI Whisper (the local open-source model, no API key required), and apply speaker diarization with **pyannote-audio**. Each speaker is displayed with a unique color and emoji for clarity. You can export the final transcript to plain text or Markdown.

## Usage
1. Install dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
2. Set the environment variable `PYANNOTE_TOKEN` to access the diarization model. You can create a token at [hf.co/pyannote](https://hf.co/pyannote).
3. Run the app:

```bash
streamlit run streamlit_app.py
```

Upload your audio file and wait for the transcription and diarization to finish. Then download the transcript in your preferred format.
