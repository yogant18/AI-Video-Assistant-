# 🎬 VideoMind — AI Video Assistant

Turn any YouTube video or local audio/video file into a transcript, summary, and a chat-ready knowledge base. Ask questions about the content and get answers pulled straight from the transcript using RAG (Retrieval-Augmented Generation).

## ✨ Features

- **Universal input** — works with YouTube URLs or local audio/video files
- **Speech-to-text** — local transcription using OpenAI Whisper (no API needed for transcription)
- **Hindi → English translation** — handles mixed Hindi-English speech
- **Auto-summarization** — generates a clean summary and an auto-titled session
- **Smart extraction** — automatically pulls out:
  - ✅ Action items
  - 🔑 Key decisions
  - ❓ Open questions
- **Chat with your video (RAG)** — ask natural-language questions and get answers grounded in the actual transcript
- **Two interfaces** — a Streamlit web UI and a CLI

## 🧠 How it works

The pipeline runs in 6 stages:

```
Audio/Video Input → Transcription → Title Generation → Summarization → Extraction → RAG Indexing
```

1. **Audio processing** — downloads/extracts audio from the input source
2. **Transcription** — converts speech to text using Whisper, with Hindi-English translation support
3. **Title generation** — generates a short title for the session
4. **Summarization** — produces a clean, readable summary
5. **Extraction** — pulls out action items, key decisions, and open questions
6. **RAG indexing** — chunks the transcript, embeds it, and stores it in a vector database for chat

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| UI | Streamlit |
| Speech-to-Text | OpenAI Whisper (local), PyTorch |
| LLM Orchestration | LangChain (LCEL), Mistral AI |
| RAG / Vector Store | ChromaDB, Sentence-Transformers, HuggingFace |
| Audio/Video handling | yt-dlp, pydub, ffmpeg |
| Translation | deep-translator |
| Export | reportlab, fpdf2 |

## 📦 Installation

1. Clone the repo
```bash
git clone https://github.com/AkarshVyas/AI-Video-Assistant-.git
cd AI-Video-Assistant-
```

2. Install dependencies
```bash
pip install -r Requirements.txt
```

3. Make sure **FFmpeg** is installed on your system (required for audio processing)

4. Create a `.env` file in the project root and add your API key(s), e.g.:
```
MISTRAL_API_KEY=your_key_here
```

## 🚀 Usage

### Option 1: Web UI (Streamlit)
```bash
streamlit run app.py
```
Paste a YouTube URL or local file path in the sidebar, choose a language, and click **Analyse**.

### Option 2: CLI
```bash
python main.py
```
You'll be prompted for a YouTube URL/file path and a language. After processing, you can chat with the transcript directly in the terminal.

## 📁 Project Structure

```
AI-Video-Assistant-/
├── app.py              # Streamlit web app
├── main.py              # CLI entry point
├── core/
│   ├── transcriber.py    # Speech-to-text (Whisper)
│   ├── summarizer.py     # Summary + title generation
│   ├── extractor.py      # Action items / decisions / questions extraction
│   └── rag_engine.py     # RAG chain (chunking, embeddings, retrieval, Q&A)
├── utils/
│   └── audio_processor.py  # Handles YouTube downloads & audio extraction
└── Requirements.txt
```

## 📌 Notes

- Transcription runs locally via Whisper — no transcription API key required.
- The LLM steps (summarization, extraction, RAG answers) use Mistral AI via LangChain — you'll need a Mistral API key.
- First run may take longer as Whisper and embedding models are downloaded.

## 📄 License

This project is open source. Feel free to fork and build on it.
