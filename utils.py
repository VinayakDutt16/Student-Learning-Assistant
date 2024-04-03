from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import streamlit as st
import elevenlabs
from transformers import AutoTokenizer, T5ForConditionalGeneration
import streamlit as st

def summarize_text(text):
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base")

    input_ids = tokenizer(text, return_tensors="pt")["input_ids"]
    outputs = model.generate(
        input_ids=input_ids,
        num_beams=4,
        max_length=128,
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

def speech_to_text_and_summarize(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )

    summarized_text = summarize_text(transcript)
    return summarized_text
load_dotenv()
api_key = os.getenv("openai_api_key")

client = OpenAI(api_key=api_key)

def get_answer(messages):
    age = 7
    cls = 2
    system_message = [{"role": "system", "content": f"Give greetings to student of age = {age} and class = {cls} after that show the subjects of his class then ask which subject he want to learn today then give the syllabus of that subject and ask him what he want he to learn from it and show him well detailed answer about his topic then give him questions about the topic he has learnt and give him correct answer if the answer is correct"}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

# elevenlabs_api_key = ''
# elevenlabs.set_api_key(elevenlabs_api_key)

# def text_to_speech(input_text, voice="Mimi", settings=None):
#     # Use Eleven Labs API for text-to-speech
#     if settings:
#         audio_data = elevenlabs.generate(input_text, voice=voice, settings=settings)
#     else:
#         audio_data = elevenlabs.generate(input_text, voice=voice)

 
#     # Save the audio file
#     webm_file_path = "temp_audio_play.mp3"
#     with open(webm_file_path, "wb") as f:
#         f.write(audio_data)
#     return webm_file_path
    
def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
