import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

if (os.getenv("GOOGLE_API_KEY") is not None):
    print("GOOGLE_API_KEY is present")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
else:
    print("GOOGLE_API_KEY is not present in env file")
    genai.configure(api_key="GOOGLE_API_KEY")


default_prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

## getting the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
default_youtube_link = "https://www.youtube.com/watch?v=tcui215ghhw"
youtube_link = st.text_input("Enter YouTube Video Link:", default_youtube_link)

prompt = st.text_area("Enter Prompt Details:", default_prompt)

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
