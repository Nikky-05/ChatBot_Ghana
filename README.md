# CatBot - GRA Support Chatbot

A RAG-powered chatbot using Gemini API to answer GRA E-commerce compliance questions.

## Features
- 🤖 AI-powered responses using Gemini 2.5 Flash
- 📚 RAG (Retrieval-Augmented Generation) with TF-IDF
- 🎨 Beautiful glassmorphism UI with Bootstrap
- 😺 Cat-themed personality
- 💬 Real-time chat interface

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_api_key_here
```

### 5. Parse FAQs (First Time Only)
```bash
python parse_faqs.py
```

### 6. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure
```
supportCat/
├── app.py                  # Flask application
├── rag_service.py          # RAG engine with Gemini
├── parse_faqs.py           # FAQ parser from DOCX
├── extracted_faqs.json     # Parsed FAQ database
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not in git)
├── templates/
│   └── index.html         # Chat UI
└── static/
    ├── css/
    │   └── style.css      # Glassmorphism styles
    └── js/
        └── script.js      # Chat functionality
```

## Technologies Used
- **Backend**: Flask, Python
- **AI**: Google Gemini 2.5 Flash
- **RAG**: scikit-learn (TF-IDF), NumPy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Document Parsing**: python-docx
