# 🎭 Indic AI App — Meme Generator, Recipe Finder & Landmark Identifier

A lightweight, **offline-friendly AI-powered app** built with **Streamlit**, designed to help users create memes, discover recipes, and identify landmarks from images, voice, and text — **with full translation support in English, Hindi, and Telugu**.

---

## ✨ Features

✅ **😂 Meme Generator**  
• Upload an image and add a custom or AI-generated meme caption.  
• Download the result with a single click.  

✅ **🍱 Recipe Finder**  
• Upload food images or describe ingredients using voice/text.  
• Automatically transcribes and detects spoken language.  
• Translates into the selected UI language.  
• Recipe logic is extensible (currently a placeholder).

✅ **📸 Landmark Identifier**  
• Upload landmark images, describe them via voice/text.  
• Auto voice language detection and translation.  
• Displays transcription and detected language.

✅ **🎙️ Auto Voice Detection & Translation**  
• Uses `Whisper` to detect spoken language from uploaded audio files.  
• Translates automatically into selected UI language using `M2M100`.

✅ **🌐 UI Language Toggle**  
• Supports full UI and translation in:  
  - English  
  - Hindi  
  - Telugu  +100 other

---

## 🛠️ Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Whisper](https://github.com/openai/whisper)
- [M2M100 Transformer](https://huggingface.co/facebook/m2m100_418M)
- PIL, Pydub, Transformers, Torch

---

## 🚀 How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd your-repo-name

🧠 AI Models Used
Whisper: For audio transcription and automatic language detection
M2M100: For multilingual text translation (100+ languages)
Install requirements
pip install -r requirements.txt
3. Run the app
streamlit run main.py
Then open http://localhost:8501 in your browser.
Feel free to fork, enhance features (like full recipe database, landmark classifier), or add more language options. PRs are welcome!
Built by Susrutha Chaparala for the Viswam.ai Summer of AI 2025 Internship, to contribute toward Indic dataset creation, open-source AI applications, and language accessibility.