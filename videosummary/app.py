import streamlit as st 
from dotenv import load_dotenv
load_dotenv() ##loads all environment variables
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""this is youtube video summarizer , this will provide transcript of whole youtube video 
summarizer in text form"""

## getting the transcript from yt videos 
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e
## getting the summary based on prompt from Google gemini
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("Youtube Transcript to detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube video link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
