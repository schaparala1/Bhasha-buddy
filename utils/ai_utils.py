# utils/ai_utils.py

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from utils.translate import translate_text

# Use Hugging Face summarization/translation models (can be cached locally)
caption_generator = pipeline("text-generation", model="gpt2", max_length=30)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Translate to English before AI processing if needed
def generate_caption(user_input, lang):
    if lang != "English":
        user_input = translate_text(user_input, lang, "English")
    result = caption_generator(user_input, max_length=30, num_return_sequences=1)
    caption = result[0]["generated_text"]
    return translate_text(caption, "English", lang) if lang != "English" else caption

def suggest_recipe_steps(user_input, lang):
    if lang != "English":
        user_input = translate_text(user_input, lang, "English")
    summary = summarizer(user_input, max_length=60, min_length=10, do_sample=False)
    suggestion = summary[0]['summary_text']
    return translate_text(suggestion, "English", lang) if lang != "English" else suggestion

def describe_landmark(user_input, lang):
    if lang != "English":
        user_input = translate_text(user_input, lang, "English")
    enriched = summarizer(user_input, max_length=50, min_length=10, do_sample=True)
    description = enriched[0]["summary_text"]
    return translate_text(description, "English", lang) if lang != "English" else description
