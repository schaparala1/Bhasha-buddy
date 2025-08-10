import streamlit as st
from PIL import Image
from io import BytesIO
from pydub import AudioSegment
import whisper
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
import base64
import os
from datetime import datetime

# ==========================
# CONFIG & STYLES
# ==========================
st.set_page_config(page_title="🎭 BhashaBuddy", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1526045478516-99145907023c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 12px;
    }
    footer {
        text-align: center;
        font-size: 14px;
        margin-top: 2rem;
        color: #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# FOLDER SETUP
# ==========================
os.makedirs("outputs", exist_ok=True)

def save_file(file_data, filename):
    """Save uploaded/generated file into outputs folder"""
    path = os.path.join("outputs", filename)
    with open(path, "wb") as f:
        f.write(file_data)
    return path

# ==========================
# LOAD MODELS
# ==========================
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")

@st.cache_resource
def load_translation_model():
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
    return tokenizer, model

whisper_model = load_whisper_model()
tokenizer, translation_model = load_translation_model()

# ==========================
# FUNCTIONS
# ==========================
def transcribe_audio(file_path):
    result = whisper_model.transcribe(file_path)
    detected_lang = result.get("language", "en")
    return result["text"], detected_lang

def translate(text, source_lang="en", target_lang="hi"):
    tokenizer.src_lang = source_lang
    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = translation_model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(target_lang))
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

def convert_audio(file):
    audio = AudioSegment.from_file(file)
    temp_path = "converted_audio.wav"
    audio.export(temp_path, format="wav")
    return temp_path

# ==========================
# UI LANGUAGES
# ==========================
supported_languages = {
    "English": "english",
    "Hindi": "hindi",
    "Telugu": "telugu",
    "Tamil": "tamil",
    "Bengali": "bengali",
    "Kannada": "kannada",
    "Malayalam": "malayalam",
    "Marathi": "marathi",
    "Gujarati": "gujarati",
    "Urdu": "urdu",
    "French": "french",
    "German": "german",
    "Spanish": "spanish",
    "Chinese (Simplified)": "chinese",
    "Japanese": "japanese",
    "Korean": "korean",
}

selected_language_label = st.selectbox("🌐 Select UI Language", list(supported_languages.keys()), index=0)
ui_language = supported_languages[selected_language_label]

# Labels
ui_text = {
    "en": {
        "title": "🎭 BhashaBuddy",
        "meme": "😂 Meme Generator",
        "recipe": "🍱 Recipe Finder",
        "landmark": "📸 Landmark Identifier",
        "audio_upload": "🎤 Upload Audio",
        "image_upload": "🖼️ Upload Image",
        "custom_text": "✍️ Enter Custom Text",
        "transcribe_result": "🗣️ Transcribed",
        "translate_result": "🌍 Translated",
        "download": "💾 Download Result",
        "submit": "🚀 Submit"
    }
}

def get_label(key):
    return ui_text.get("en", {}).get(key, key)

# ==========================
# APP TITLE
# ==========================
st.title(get_label("title"))

# ==========================
# TABS
# ==========================
tab1, tab2, tab3 = st.tabs([get_label("meme"), get_label("recipe"), get_label("landmark")])

# Meme Tab
with tab1:
    with st.form("meme_form"):
        img_file = st.file_uploader(get_label("image_upload"), type=["jpg", "jpeg", "png"])
        custom_text = st.text_input(get_label("custom_text"))
        submitted = st.form_submit_button(get_label("submit"))
        
        if submitted and img_file:
            image = Image.open(img_file)
            st.image(image, caption="Uploaded Image")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_file(img_file.read(), f"meme_{timestamp}.png")
            if custom_text:
                st.markdown(f"### Meme: {custom_text}")
                save_file(custom_text.encode(), f"meme_text_{timestamp}.txt")
            st.success("✅ Meme saved to outputs folder")

# Recipe Tab
with tab2:
    with st.form("recipe_form"):
        img_file = st.file_uploader(get_label("image_upload") + " (Recipe)", type=["jpg", "jpeg", "png"])
        text_input = st.text_area(get_label("custom_text") + " (Recipe)")
        audio_file = st.file_uploader(get_label("audio_upload") + " (Recipe)", type=["mp3", "wav"])
        submitted = st.form_submit_button(get_label("submit"))

        if submitted:
            if audio_file:
                st.audio(audio_file)
                converted = convert_audio(audio_file)
                transcribed, detected_lang = transcribe_audio(converted)
                st.success(f"{get_label('transcribe_result')}: {transcribed}")
                st.info(f"🧭 Detected Language: {detected_lang.upper()}")
                translated = translate(transcribed, source_lang=detected_lang, target_lang=ui_language)
                text_input = translated
                save_file(transcribed.encode(), f"recipe_transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

            if img_file:
                st.image(Image.open(img_file), caption="Recipe Image")
                save_file(img_file.read(), f"recipe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

            if text_input:
                st.success("🍽️ Recipes coming soon (placeholder)")
                save_file(text_input.encode(), f"recipe_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            st.success("✅ Recipe data saved to outputs folder")

# Landmark Tab
with tab3:
    with st.form("landmark_form"):
        img_file = st.file_uploader(get_label("image_upload") + " (Landmark)", type=["jpg", "jpeg", "png"])
        text_input = st.text_area(get_label("custom_text") + " (Landmark)")
        audio_file = st.file_uploader(get_label("audio_upload"), type=["mp3", "wav"])
        submitted = st.form_submit_button(get_label("submit"))

        if submitted:
            if audio_file:
                st.audio(audio_file)
                converted = convert_audio(audio_file)
                transcribed, detected_lang = transcribe_audio(converted)
                st.success(f"{get_label('transcribe_result')}: {transcribed}")
                st.info(f"🧭 Detected Language: {detected_lang.upper()}")
                translated = translate(transcribed, source_lang=detected_lang, target_lang=ui_language)
                save_file(transcribed.encode(), f"landmark_transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

            if img_file:
                st.image(Image.open(img_file), caption="Landmark Image")
                save_file(img_file.read(), f"landmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

            if text_input:
                st.markdown(f"**📝 Text Input:** {text_input}")
                save_file(text_input.encode(), f"landmark_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            st.success("✅ Landmark data saved to outputs folder")

# ==========================
# FOOTER
# ==========================
st.markdown("<footer>💡 Built by Susrutha</footer>", unsafe_allow_html=True)
