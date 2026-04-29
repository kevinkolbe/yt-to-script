import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    pattern = r'(?:v=|\/|be\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_script_layout(video_id):
    try:
        # We call the function directly from the library name
        # This is the most stable 'old school' way to do it
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        
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
st.write("Turn your video into a clean script layout instantly.")

video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    video_id = extract_video_id(video_url)
    if video_id:
        if st.button("Generate Script"):
            with st.spinner("Processing your video..."):
                final_script = get_script_layout(video_id)
                
                if "Error:" in final_script:
                    st.error("Transcript not found. Make sure the video has 'Captions' (CC) available on YouTube!")
                else:
                    st.subheader("Formatted Script")
                    st.text_area("Your Script Layout:", value=final_script, height=400)
                    
                    st.download_button(
                        label="Download as Text File",
                        data=final_script,
                        file_name="video_script.txt",
                        mime="text/plain"
                    )
    else:
        st.warning("Please enter a valid YouTube URL.")
