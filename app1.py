import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text_and_summarize, summarize_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import requests
import pandas as pd
from googleapiclient.discovery import build

st.session_state.student_interests = ["Innovation", "Technology"]
def news(interests):
    title = []
    urla = []
    news_api_key = ""  # Replace with your News API key
    for interest in interests:
        url = f"https://newsapi.org/v2/everything?q={interest}&apiKey={news_api_key}"
        news_data = requests.get(url).json()
        articles = news_data["articles"][:5]  
        for article in articles:
            title.append(article["title"])
            urla.append(article["url"])
    return pd.DataFrame({"Title": title, "URL": urla})

# To-do list in the sidebar
def suggest_youtube_video(query):
    youtube = build("youtube", "v3", developerKey="")

    # Search for videos based on the query
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id, snippet",
        maxResults=1
    ).execute()

    # Extract the video ID and snippet details from the search result
    video_id = search_response["items"][0]["id"]["videoId"]
    video_title = search_response["items"][0]["snippet"]["title"]
    thumbnail_url = search_response["items"][0]["snippet"]["thumbnails"]["medium"]["url"]

    # Display the video thumbnail
    st.image(thumbnail_url, caption=f"{video_title}", use_column_width=True)

    # Construct the YouTube video URL
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # Display clickable link below the thumbnail
    st.markdown(f"[Watch on YouTube]({video_url})")

    return video_url

# Sidebar with recent news
st.sidebar.title("Recent News")
st.sidebar.write("News according to your interests : ")

recent_news_df = news(interests=st.session_state.student_interests)
for index, row in recent_news_df.iterrows():
    st.sidebar.markdown(f"**{index + 1}. [{row['Title']}]({row['URL']})**")
# Float feature initialization
float_init()

st.session_state.query_counter = 0
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi Student, How are you!!!"}
        ]
        st.session_state.first_query = True
        st.session_state.student_interests = ["Innovation", "Technology"]

initialize_session_state()
st.sidebar.title("Hobbies")
interests_query = '+'.join(st.session_state.student_interests)
youtube_link = f"https://www.youtube.com/results?search_query={interests_query}"
st.sidebar.markdown(f"[Your Interests]({youtube_link})")

st.title("Study bot 🤖")
st.write("Your dedicated learning companion, tailored to enhance your educational journey.")
# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Modified function for speech to text and summarization
        summarized_transcript = speech_to_text_and_summarize(webm_file_path)

        if summarized_transcript:
            st.session_state.messages.append({"role": "user", "content": summarized_transcript})
            with st.chat_message("user"):
                st.write(summarized_transcript)
            os.remove(webm_file_path)
       

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
            
        if not st.session_state.first_query:
            # Suggest YouTube video based on the final response after the first query
            with st.spinner("Searching for relevant YouTube video..."):
                video_url = suggest_youtube_video(final_response)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

        st.session_state.first_query = False

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem;")


