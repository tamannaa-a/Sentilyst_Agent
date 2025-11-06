# 🧠 Sentilyst — Empathy Coach & Sentiment Forecasting AI

> **A voice-enabled, emotion-aware conversational AI** that detects mood, generates empathetic replies, and visualizes emotional trends interactively.

---

## 🌟 Overview

**Sentilyst** is an advanced AI-driven emotional support assistant that helps users **understand, track, and improve their moods** through natural conversations.  
It combines **sentiment analysis**, **empathetic text generation**, **speech interaction**, and **interactive data visualization** into a single unified experience.

Users can **type or speak** their emotions, and Sentilyst:
- Detects their **mood sentiment** (positive / neutral / negative),
- Responds with **kind, supportive messages**,
- **Forecasts emotional trends** for the upcoming days, and
- Displays **interactive mood graphs**.

---

## 🎯 Features

✅ Dual Input — Text 💬 or Voice 🎙️  
✅ AI Responses — Empathetic, encouraging, non-repetitive  
✅ Sentiment Analysis — Real-time emotion detection using NLP  
✅ Mood Forecast — 7-day sentiment prediction  
✅ Voice Output — AI speaks back via Text-to-Speech  
✅ Historical Tracking — Stores daily mood history in SQLite  
✅ Professional Dashboard — Interactive Plotly graphs in Streamlit  
✅ Works Fully Offline (No API Keys Needed)

---

## 🏗️ Architecture


---

## 🤖 Models & Tools Used

| Component | Purpose | Library/Model |
|------------|----------|---------------|
| **Text Sentiment Detection** | Analyzes mood from user text | `TextBlob` |
| **Empathetic Reply Generation** | Generates kind, supportive messages | `google/flan-t5-small` (Hugging Face Transformers) |
| **Voice Input (Speech-to-Text)** | Captures spoken input | `SpeechRecognition` + `PyAudio` |
| **Voice Output (Text-to-Speech)** | Speaks AI replies aloud | `gTTS` |
| **Data Storage** | Saves sentiment history | `SQLite3` |
| **Visualization** | Displays interactive sentiment graphs | `Plotly` |
| **User Interface** | Builds the professional dashboard | `Streamlit` |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/tamannaa-a/Sentilyst.git
cd Sentilyst
