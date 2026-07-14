import streamlit as st
import requests
from gtts import gTTS
import random
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="English Every Day", layout="centered")

# --- API HELPERS ---
def get_word_data(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    return None

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("pronunciation.mp3")
    return "pronunciation.mp3"

# --- UI SETUP & STATE ---
st.title("📚 English Every Day")

if 'current_word_data' not in st.session_state:
    st.session_state.current_word_data = None
if 'history' not in st.session_state:
    st.session_state.history = []

# --- MAIN LOGIC ---
if st.button("🌟 Ready to learn a word?"):
    words = [
    "abundant", "adverse", "advocate", "aesthetic", "affable", "alleviate", "ambiguous", "ambivalent", "amiable", "anecdote",
    "anomaly", "apathetic", "ardent", "articulate", "audacious", "austere", "benevolent", "benign", "biased", "brevity",
    "candid", "capricious", "catalyst", "cautious", "celestial", "chronic", "coherent", "collaborate", "commend", "complacent",
    "concise", "condone", "conspicuous", "contempt", "conventional", "corroborate", "cryptic", "curtail", "cynical", "decorum",
    "deference", "depict", "deride", "desolate", "diligent", "disdain", "disparity", "divisive", "dogmatic", "durable",
    "eccentric", "eclectic", "effervescent", "eloquent", "elusive", "emancipate", "empathy", "empirical", "enigma", "enthusiastic",
    "ephemeral", "equivocal", "erudite", "esoteric", "eulogy", "evasive", "exacerbate", "exemplary", "exonerate", "expedite",
    "extol", "fallacious", "fastidious", "feasible", "fervent", "fickle", "flourish", "formidable", "fortitude", "frivolous",
    "garrulous", "genial", "gratitude", "gregarious", "haphazard", "hesitant", "hypothetical", "impartial", "impeccable", "impetuous",
    "improvise", "incisive", "indifferent", "inevitable", "ingenious", "inherent", "innocuous", "innovative", "insatiable", "intrepid"
]
    word = random.choice(words) 
    st.session_state.current_word_data = get_word_data(word)
    
   

if st.session_state.current_word_data:
    data = st.session_state.current_word_data
    word = data['word']
    meaning = data['meanings'][0]['definitions'][0]['definition']
    
    st.subheader(f"Word: {word.capitalize()}")
    st.write(f"**Meaning:** {meaning}")
    
    if st.button("🔊 Play Pronunciation"):
        audio_path = text_to_speech(word)
        st.audio(audio_path)
    
    if st.button("❤️ Save to History"):
        if word not in [item['word'] for item in st.session_state.history]:
            st.session_state.history.append({'word': word, 'meaning': meaning})
            st.success("Word saved to your collection!")


# --- HISTORY SECTION ---
st.divider()
st.subheader("📖 Your Learning History")
for item in st.session_state.history:
    with st.expander(f"Review: {item['word']}"):
        st.write(f"Definition: {item['meaning']}")