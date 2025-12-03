import streamlit as st
from pathlib import Path
import tempfile
import sys 
import os 
import pandas as pd

# --- Project path setup ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Modules
from src.audio.enhancer import enhance_audio
from src.transcription.whisper_transcriber import WhisperTranscriber
from src.analysis.summarizer import MeetingSummarizer
from src.analysis.task_extractor import TaskExtractor
from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.research.topic_extractor import TopicExtractor
from src.research.web_searcher import WebSearcher
from src.dashboard.components import record_audio_stream , save_recording

# ================= UI CONFIG =================
st.set_page_config(
    page_title="MeetingMind",
    layout="wide",
    page_icon="💼"
)

# ================= CUSTOM STYLES =================
st.markdown(
    """
    <style>
    /* Page background */
    .main {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* Titles */
    .title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ================= HEADER =================
st.markdown("<div class='title'>💭 💼 MeetingMind – Smart AI Meeting Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Transform your meetings into structured knowledge</div>", unsafe_allow_html=True)

# ================= SESSION STATES =================
if "recording" not in st.session_state:
    st.session_state.recording = False
    st.session_state.stream = None
    st.session_state.audio_data = None

if "processed" not in st.session_state:
    st.session_state.processed = False

if "results" not in st.session_state:
    st.session_state.results = {}

# ================= MAIN CARD =================
with st.sidebar:

    st.markdown("### Upload or Record Your Meeting Audio")
    audio_file = st.file_uploader("🎧 Upload Audio (mp3/wav)", type=["mp3","wav"])
# ================= PROCESS BUTTON =================

st.markdown("<div class='subtitle'>📌 When your audio is ready, click Process Meeting to analyze it.</div>", unsafe_allow_html=True)
process_button = st.button("🚀 Start Processing Meeting", use_container_width=True)

# ================= MAIN PROCESSING =================
if process_button and audio_file:
    with st.spinner("Processing meeting data..."):
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        if isinstance(audio_file, str):
            audio_path = audio_file
        else:
            temp_audio.write(audio_file.read())
            audio_path = temp_audio.name

        enhanced_audio_path = enhance_audio(audio_path)

        transcriber = WhisperTranscriber()
        transcript = transcriber.transcribe(enhanced_audio_path)

        summarizer = MeetingSummarizer()
        summary = summarizer.summarize(transcript)

        task_extractor = TaskExtractor()
        tasks = task_extractor.extract_tasks(transcript)

        sentiment_analyzer = SentimentAnalyzer()
        sentiment = sentiment_analyzer.analyze_sentiment(transcript)

        topic_extractor = TopicExtractor()
        topic = topic_extractor.extract_topic(transcript)

        web_searcher = WebSearcher()
        web_results = web_searcher.search(topic)

        st.session_state.results = {
            "transcript": transcript,
            "summary": summary,
            "tasks": tasks,
            "sentiment": sentiment,
            "topic": topic,
            "web_results": web_results
        }

        st.session_state.processed = True

# ================= RESULTS VIEW =================
if st.session_state.processed:
    tabs = st.tabs(["📝 Transcript", "📌 Summary", "✅ Tasks", "😊 Sentiment", "🌍 Research"])

    with tabs[0]:
        st.markdown(st.session_state.results["transcript"])

    with tabs[1]:
        st.markdown(st.session_state.results["summary"], unsafe_allow_html=True)

    with tabs[2]:
        tasks = st.session_state.results["tasks"]
        if tasks:
            st.dataframe(pd.DataFrame(tasks), use_container_width=True)
        else:
            st.info("No tasks detected")

    with tabs[3]:
        sentiment = st.session_state.results["sentiment"]
        overall = sentiment["sentiment"]["overall_sentiment"]
        emotions = sentiment["sentiment"]["emotions"]

        color = "gray"
        if overall.lower() == "positive":
            color = "green"
        elif overall.lower() == "negative":
            color = "red"
        elif overall.lower() == "neutral":
            color = "orange"

        st.markdown(f"**Overall Sentiment:** <span style='color:{color}; font-weight:bold;'>{overall}</span>", unsafe_allow_html=True)
        if emotions:
            badges = ", ".join(emotions)
            st.markdown(f"**Detected Emotions:** {badges}", unsafe_allow_html=True)

    with tabs[4]:
        topic = st.session_state.results["topic"]
        st.markdown(f"### Main Topic: {topic}")
        st.markdown(st.session_state.results["web_results"])
