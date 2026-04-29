import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    # Regex to find the video ID from various YouTube URL formats
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_script_layout(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        script = ""
        for entry in transcript:
            # Formatting as [MM:SS] Text
            start_time = int(entry['start'])
            minutes = start_time // 60
            seconds = start_time % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            script += f"{timestamp} {entry['text']}\n"
        return script
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("YouTube to Script Converter")
st.write("Paste a YouTube link below to generate a clean script layout.")

video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    video_id = extract_video_id(video_url)
    if video_id:
        if st.button("Generate Script"):
            with st.spinner("Pulling transcript..."):
                final_script = get_script_layout(video_id)
                
                if "Error:" in final_script:
                    st.error(final_script)
                else:
                    st.subheader("Formatted Script")
                    st.text_area("Copy/Paste this into your blog or PDF:", 
                                 value=final_script, height=400)
                    
                    st.download_button(
                        label="Download as Text File",
                        data=final_script,
                        file_name="transcript_script.txt",
                        mime="text/plain"
                    )
    else:
        st.warning("Please enter a valid YouTube URL.")
