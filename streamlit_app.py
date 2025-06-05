import streamlit as st
import whisper
from pyannote.audio import Pipeline
import os
import tempfile
from datetime import timedelta

# Assign colors and icons
COLORS = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe"]
ICONS = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🙂", "🙃", "😉"]

@st.cache_resource
def load_models():
    token = os.getenv("PYANNOTE_TOKEN")
    if not token:
        st.warning("PYANNOTE_TOKEN is not set")
        st.stop()
    whisper_model = whisper.load_model("base")
    diarization_pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization@2.1",
        use_auth_token=token,
    )
    return whisper_model, diarization_pipeline

whisper_model, diarization_pipeline = load_models()

st.title("Meeting Transcription Tool")
uploaded_file = st.file_uploader("Upload audio", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Transcribing..."):
        result = whisper_model.transcribe(tmp_path)

    with st.spinner("Diarizing speakers..."):
        diarization = diarization_pipeline(tmp_path)

    # map speaker to color/icon
    speaker_labels = sorted(set([label for _, label in diarization.itertracks(yield_label=True)]))
    color_map = {spk: COLORS[i % len(COLORS)] for i, spk in enumerate(speaker_labels)}
    icon_map = {spk: ICONS[i % len(ICONS)] for i, spk in enumerate(speaker_labels)}

    transcript_txt = []
    transcript_md = []

    from pyannote.core import Segment
    for segment in result["segments"]:
        seg = Segment(segment['start'], segment['end'])
        speaker = None
        max_overlap = 0
        for turn, _, label in diarization.itertracks(yield_label=True):
            overlap = seg & turn
            if overlap.duration > max_overlap:
                speaker = label
                max_overlap = overlap.duration
        if speaker is None:
            speaker = "Speaker"
        start_time = str(timedelta(seconds=int(segment['start'])))
        line_txt = f"[{start_time}] {speaker}: {segment['text'].strip()}"
        line_md = f"<span style='color:{color_map[speaker]}; font-weight:bold'>{icon_map[speaker]} {speaker}</span> <span style='color:gray'>[{start_time}]</span> {segment['text'].strip()}"
        transcript_txt.append(line_txt)
        transcript_md.append(line_md)
        st.markdown(line_md, unsafe_allow_html=True)

    txt_content = "\n".join(transcript_txt)
    md_content = "\n\n".join(transcript_md)

    st.download_button("Download TXT", txt_content, file_name="transcript.txt")
    st.download_button("Download MD", md_content, file_name="transcript.md")
    os.remove(tmp_path)

