PDF Insights is a Python-based application that extracts text from PDF documents, generates concise summaries, and visualizes key insights using modern LLMs such as Hugging Face and Groq.

## 📌 Overview

**PDF Summary Visualizer** is a Python-based application that extracts text from PDF documents, generates meaningful summaries, and visualizes insights using charts and visual elements.

The project integrates **Hugging Face models** and **Groq-powered LLMs** to improve text understanding and summarization quality, making it easier to analyze large PDF documents efficiently.

---

## ✨ Features

- 📄 Extracts text content from PDF files  
- 🧠 Generates concise summaries from extracted text  
- 📊 Visualizes insights using charts and graphs  
- 🤖 Supports Hugging Face and Groq-based models  
- 🖥️ Simple and interactive Python interface  

---

## 🛠️ Tech Stack

- Python  
- Hugging Face Transformers  
- Groq LLM  
- PDF Processing Libraries  
- Matplotlib / Visualization Tools  

---

## 📂 Project Structure

```text
├── app.py                         # Main application entry point
├── visualization_tool_with_hf.py  # Visualization using Hugging Face models
├── visualization_with_groq.py     # Visualization using Groq LLM
├── requirements.txt               # Project dependencies
├── README.md                      # Project documentation
└── .gitignore

▶️ Installation & Setup
Prerequisites
Python 3.12
pip
Virtual environment (recommended)

1️⃣ Clone the Repository
git clone https://github.com/dearnidhi/PDF-Summary-Visualizer.git
cd PDF-Summary-Visualizer

2️⃣ Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Run the Application
python app.py


Once running, the application allows you to:
Upload PDF files
Extract and summarize text
Visualize insights interactively

⚠️ Notes

Intended for educational and experimental use
Performance depends on PDF size and model selection
Requires internet access for LLM-based processing
Not optimized for large-scale production workloads
