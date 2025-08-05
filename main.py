import streamlit as st
from PIL import Image
from io import BytesIO
from pydub import AudioSegment
import whisper
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
import base64

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
    </style>
    """,
    unsafe_allow_html=True
)


# Load models
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

# Functions
def transcribe_audio(file_path):
    result = whisper_model.transcribe(file_path)
    return result["text"]

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

# UI language selector
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
    "Chinese (Simplified)": "zh",
    "Japanese": "japanese",
    "Korean": "korea",
    # Add more if needed
}
selected_language_label = st.selectbox("🌐 Select UI Language", list(supported_languages.keys()), index=0)
ui_language = supported_languages[selected_language_label]



# Translate text helper
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
        "download": "💾 Download Result"
    },
    "hi": {},
    "te": {}
}

# Fallback for untranslated
def get_label(key):
    return ui_text.get(ui_language, {}).get(key, ui_text["en"][key])

# App title
st.title(get_label("title"))

# Tabs for features
tab1, tab2, tab3 = st.tabs([get_label("meme"), get_label("recipe"), get_label("landmark")])

with tab1:
    img_file = st.file_uploader(get_label("image_upload"), type=["jpg", "jpeg", "png"])
    custom_text = st.text_input(get_label("custom_text"))
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image")
        if custom_text:
            st.markdown(f"### Meme: {custom_text}")
        st.download_button(get_label("download"), img_file.read(), file_name="meme.png")

with tab2:
    st.header(get_label("recipe"))
    img_file = st.file_uploader(get_label("image_upload") + " (Recipe)", type=["jpg", "jpeg", "png"])
    text_input = st.text_area(get_label("custom_text") + " (Recipe)")
    audio_file = st.file_uploader(get_label("audio_upload") + " (Recipe)", type=["mp3", "wav"])

    # Voice Input
    if audio_file:
        st.audio(audio_file)
        converted = convert_audio(audio_file)
        transcribed, detected_lang = transcribe_audio(converted)
        st.success(f"{get_label('transcribe_result')}: {transcribed}")
        st.info(f"🧭 Detected Language: {detected_lang.upper()}")
        translated = translate(transcribed, source_lang=detected_lang, target_lang=ui_language)
        text_input = translated  # Optional: Autofill recipe text input with translated voice

    # Text or image input
    if img_file:
        st.image(Image.open(img_file), caption="Recipe Image")
    
    if text_input:
        st.success("🍽️ Recipes coming soon (placeholder)")
        st.download_button(get_label("download"), text_input.encode(), file_name="recipe.txt")


with tab3:
    img_file = st.file_uploader(get_label("image_upload") + " (Landmark)", type=["jpg", "jpeg", "png"])
    text_input = st.text_area(get_label("custom_text") + " (Landmark)")
    audio_file = st.file_uploader(get_label("audio_upload"), type=["mp3", "wav"])

    if audio_file:
        st.audio(audio_file)
        converted = convert_audio(audio_file)
        transcribed, detected_lang = transcribe_audio(converted)
        st.success(f"{get_label('transcribe_result')}: {transcribed}")
        st.info(f"🧭 Detected Language: {detected_lang.upper()}")
        translated = translate(transcribed, source_lang=detected_lang, target_lang=ui_language)

    if img_file:
        st.image(Image.open(img_file), caption="Landmark Image")
        st.success("📍 Landmark identification coming soon")

    if text_input:
        st.markdown(f"**📝 Text Input:** {text_input}")
        st.download_button(get_label("download"), text_input.encode(), file_name="landmark.txt")
# Footer
st.markdown("---")
st.markdown("<center>👩‍💻 Built by <b>Susrutha Chaparala</b> | Summer of AI 2025</center>", unsafe_allow_html=True)