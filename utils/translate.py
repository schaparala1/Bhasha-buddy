# utils/translate.py

from transformers import pipeline

# Load multilingual translation pipeline (offline supportable)
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")

# Language Codes (NLLB format)
lang_map = {
    "English": "eng_Latn",
    "Telugu": "tel_Telu",
    "Hindi": "hin_Deva"
}

def translate_text(text, src_lang, tgt_lang):
    src = lang_map.get(src_lang, "eng_Latn")
    tgt = lang_map.get(tgt_lang, "eng_Latn")
    result = translator(text, src_lang=src, tgt_lang=tgt)
    return result[0]["translation_text"]
