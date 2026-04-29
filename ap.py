import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    pattern = r'(?:v=|\/|be\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_script_layout(video_id):
    try:
        # We try a specific language order to bypass some filtering
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Look for manual English, then auto English, then anything else
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                # Fallback to the first available transcript in the list
                transcript = next(iter(transcript_list))
            
        transcript_data = transcript.fetch()
        
        script = ""
        for entry in transcript_data:
            start_time = int(entry['start'])
            minutes = start_time // 60
            seconds = start_time % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            script += f"{timestamp} {entry['text']}\n"
        return script
    except Exception as e:
        # If we get a "RequestBlocked" or "Proxy" error, we know it's a Cloud Ban
        error_msg = str(e)
        if "RequestBlocked" in error_msg or "too many requests" in error_msg.lower():
            return "ERROR_CLOUD_BAN"
        return f"Error: {error_msg}"

# Streamlit UI
st.set_page_config(page_title="YouTube to Script", page_icon="🎥")
st.title("YouTube to Script Converter")
st.write("Turn your video into a formatted script for blogs or PDFs.")

video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    video_id = extract_video_id(video_url)
    if video_id:
        if st.button("Generate Script"):
            with st.spinner("Extracting..."):
                final_script = get_script_layout(video_id)
                
                if final_script == "ERROR_CLOUD_BAN":
                    st.error("⚠️ YouTube is currently blocking this server's IP address. This happens sometimes with free cloud hosting.")
                    st.info("Try again in a few minutes, or use a different video link to 'wake' the connection.")
                elif "Error:" in final_script:
                    st.error(f"Could not find transcript. {final_script}")
                else:
                    st.subheader("Formatted Script")
                    st.text_area("Your Script Layout:", value=final_script, height=400)
                    
                    st.download_button(
                        label="Download Script",
                        data=final_script,
                        file_name="video_script.txt"
                    )
    else:
        st.warning("Please enter a valid YouTube URL.")
