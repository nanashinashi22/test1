# Streamlit Meeting Transcription Tool

This app lets you upload an MP3 or WAV file, transcribe it using OpenAI Whisper, and apply speaker diarization with **pyannote-audio**. Each speaker is displayed with a unique color and emoji for clarity. You can export the final transcript to plain text or Markdown.

## Usage
1. Install dependencies (Streamlit, openai-whisper, pyannote-audio, etc.).
2. Set the environment variables `OPENAI_API_KEY` and `PYANNOTE_TOKEN` for access to the models.
3. Run the app:

```bash
streamlit run streamlit_app.py
```

Upload your audio file and wait for the transcription and diarization to finish. Then download the transcript in your preferred format.
