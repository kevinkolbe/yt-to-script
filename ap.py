import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    pattern = r'(?:v=|\/|be\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_script_layout(video_id):
    try:
        # The NEW 2026 way to call the transcript
        ytt_api = YouTubeTranscriptApi()
        # We try to fetch the transcript data
        transcript_data = ytt_api.fetch(video_id).to_raw_data()
        
        script = ""
        for entry in transcript_data:
            start_time = int(entry['start'])
            minutes = start_time // 60
            seconds = start_time % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            script += f"{timestamp} {entry['text']}\n"
        return script
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="YouTube to Script", page_icon="🎥")
st.title("YouTube to Script Converter")
st.write("Turn your video into a formatted script for blogs or PDFs.")

video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    video_id = extract_video_id(video_url)
    if video_id:
        if st.button("Generate Script"):
            with st.spinner("Processing your video..."):
                final_script = get_script_layout(video_id)
                
                if "Error:" in final_script:
                    st.error("Transcript not found. Tip: Check if 'Captions' are available on the YouTube video itself!")
                else:
                    st.subheader("Formatted Script")
                    st.text_area("Your Script Layout:", value=final_script, height=400)
                    
                    st.download_button(
                        label="Download Script",
                        data=final_script,
                        file_name="kevin_kolbe_script.txt",
                        mime="text/plain"
                    )
    else:
        st.warning("Please enter a valid YouTube URL.")
