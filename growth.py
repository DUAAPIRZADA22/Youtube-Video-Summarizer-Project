import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
from transformers import pipeline  # type: ignore
import re

# Function to extract video transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript])
        return text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to summarize text using AI
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Split long text into chunks for summarization
    max_input = 1024  # BART model ka max token limit
    text_chunks = [text[i:i+max_input] for i in range(0, len(text), max_input)]

    summaries = []
    for chunk in text_chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    return " ".join(summaries)

# Extract YouTube Video ID
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# Streamlit UI
st.set_page_config(page_title="YouTube Video Summarizer", page_icon="🎥", layout="centered")

st.markdown(
    """
    <style>
        .main {
            background-color: #f4f4f4;
        }
        h1 {
            color: #ff4b4b;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #444;
            font-weight: bold;
        }
        .stTextInput {
            border-radius: 10px;
            border: 2px solid #ff4b4b;
            padding: 8px;
        }
        .stButton>button {
            border-radius: 10px;
            background-color: #ff4b4b;
            color: white;
            font-size: 16px;
            padding: 10px;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #ff1a1a;
        }
        .summary-box {
            padding: 15px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("YouTube Video Summarizer 🎥")
st.markdown('<p class="subtitle">by <span style="color:#ff4b4b;">Duaa Pirzada</span></p>', unsafe_allow_html=True)

video_url = st.text_input("🔗 Enter YouTube Video URL:")

if video_url:
    video_id = extract_video_id(video_url)

    if video_id:
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        # Get transcript
        transcript = get_transcript(video_id)

        if "Error" not in transcript:
            st.subheader("📝 Original Transcript:")
            st.markdown(f'<div class="summary-box">{transcript[:1000]}...</div>', unsafe_allow_html=True)

            # Generate summary
            summary = summarize_text(transcript)
            st.subheader("📌 Summary:")
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
        else:
            st.error("⚠️ Could not fetch transcript. Make sure the video has subtitles.")
    else:
        st.error("❌ Invalid YouTube URL. Please enter a correct link.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p><strong>Developed by <span style="color:#ff4b4b;">Duaa Pirzada</span></strong></p>
        <p>📧 <a href="mailto:pirzadaduaa87@gmail.com" target="_blank">Email</a></p>
        <p>🐦 <a href="https://x.com/DuaaPirzada" target="_blank">Twitter Profile</a></p>
        <p>🔗 <a href="https://www.linkedin.com/in/duaa-pirzada-52a1062aa/" target="_blank">LinkedIn Profile</a></p>
    </div>
    """,
    unsafe_allow_html=True
)



