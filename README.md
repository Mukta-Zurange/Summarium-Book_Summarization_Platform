# 📚 Summarium – AI-Powered Book Summarization Platform

**Summarium** is an AI-powered web application that helps users quickly understand books and large textual documents by generating intelligent summaries using **Natural Language Processing (NLP)** and **Large Language Models (LLMs)**.

The platform supports PDF files, TXT files, and direct text input. Users can generate summaries in different lengths and formats and use additional AI-powered learning features such as **mind maps, quizzes, and an AI chatbot**.

---

## 🎯 Project Objective

Reading lengthy books and documents can be time-consuming, especially when users need to quickly identify the important concepts and key ideas.

Summarium addresses this problem by automatically processing large amounts of text and generating meaningful summaries while preserving the important information. It also provides interactive features that help users understand and revise the content more effectively.

---

## ✨ Key Features

### 🔐 User Authentication

* User registration and login
* Password recovery using security questions
* Role-based access control
* Separate user and admin functionality

### 📄 Multiple Input Methods

Users can provide content through:

* 📕 PDF upload
* 📄 TXT file upload
* 📝 Direct text input

Each uploaded or submitted document is assigned a unique identifier for further processing.

### 🤖 AI-Powered Summarization

Summarium generates summaries based on user preferences.

**Summary formats:**

* Bullet points
* Paragraph format

**Summary lengths:**

* Short
* Medium
* Detailed

Additional functionality includes:

* Summary regeneration
* Summary history
* Copy summary to clipboard
* Download summary as PDF

### 🧠 Mind Map Generation

The platform extracts important concepts from the content and generates a visual representation of their relationships.

Users can use mind maps to understand the structure and connections between important ideas in a document.

### ❓ AI Quiz Generation

Summarium can generate quizzes from the processed content.

The quiz module provides:

* AI-generated questions
* Automatic answer evaluation
* Score calculation
* Identification of incorrect answers
* Correct answer display

### 💬 AI Chatbot

Users can interact with the system using an AI-powered chatbot to ask questions and obtain assistance related to the processed content.

### 📚 Book Repository

Uploaded books and documents are stored in a centralized repository.

The system provides:

* Book ID tracking
* Book title and author information
* Search functionality
* Duplicate upload prevention

### 👨‍💼 Admin Dashboard

Administrators can manage and monitor the platform, including:

* Registered users
* Uploaded books
* Summary statistics
* User management
* Book management

---

## 🔄 System Workflow

```text
                User
                  │
                  ▼
       PDF / TXT / Direct Text
                  │
                  ▼
          Text Extraction
                  │
                  ▼
        Text Preprocessing
                  │
                  ▼
             Chunking
                  │
                  ▼
       Chunk-level Summarization
                  │
                  ▼
        Final Summary Generation
                  │
                  ▼
            MySQL Database
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
     Mind Map    Quiz     AI Chatbot
```

---

## 🧠 NLP & Summarization Pipeline

Large documents cannot always be processed by an LLM in a single request because of context/token limitations. Therefore, Summarium follows a chunk-based processing approach.

### 1. Text Extraction

The application extracts textual content from uploaded PDF/TXT files or accepts text entered directly by the user.

### 2. Text Preprocessing

The extracted content is cleaned and normalized before being sent for summarization.

This includes:

* Removing unwanted characters
* Cleaning formatting
* Normalizing text
* Validating the extracted content

### 3. Text Chunking

Large documents are divided into smaller manageable chunks.

This allows the application to process lengthy documents without exceeding the context limitations of the language model.

### 4. Chunk Summarization

Each chunk is independently processed by the LLM to generate an intermediate summary.

### 5. Final Summary Generation

The intermediate summaries are combined and processed to produce a coherent final summary according to the user's selected length and format.

### 6. Additional AI Features

The processed content can then be used for:

* Mind-map generation
* Quiz generation
* AI chatbot interaction

---

## 🏗️ Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI
* Uvicorn

### AI / NLP

* Natural Language Processing
* Large Language Models
* Ollama
* Groq API
* Chunk-based summarization

### Database

* MySQL

### Other Tools & Libraries

* PDF/text extraction libraries
* Python-based utility modules
* Environment variables using `.env`

---

## 📁 Project Structure

```text
Summarium-Book_Summarization_Platform/
│
├── static/
│   ├── CSS
│   ├── JavaScript
│   └── other frontend assets
│
├── templates/
│   └── HTML templates
│
├── app.py
│   └── Main FastAPI application
│
├── auth_utils.py
│   └── Authentication and authorization utilities
│
├── chunking.py
│   └── Text chunking logic
│
├── database.py
│   └── Database connection and operations
│
├── extractor.py
│   └── Text extraction from uploaded content
│
├── models.py
│   └── Data models
│
├── preprocessing.py
│   └── Text preprocessing and cleaning
│
├── summarizer.py
│   └── AI-based summarization logic
│
├── utils.py
│   └── Supporting utility functions
│
├── book_summarizer_dump.sql
│   └── MySQL database dump
│
├── requirements.txt
│   └── Python dependencies
│
└── .env.example
    └── Environment variable template
```

---

## 🗄️ Database

The application uses **MySQL** for storing application and summarization data.

Major entities include:

* Users
* Books
* Raw extracted text
* Pasted text
* Chunk summaries
* Final summaries

The database helps maintain user information, uploaded content, summary history, and other application data.

---

## ⚙️ Installation

### Prerequisites

Make sure the following are installed:

* Python 3.10+
* MySQL
* Ollama

You will also need a **Groq API key** for the Groq-powered LLM functionality.

### 1. Clone the Repository

```bash
git clone https://github.com/Mukta-Zurange/Summarium-Book_Summarization_Platform.git

cd Summarium-Book_Summarization_Platform
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=book_summarizer

GROQ_API_KEY=your_groq_api_key
OLLAMA_MODEL=llama3
```

### 5. Configure the Database

Create the MySQL database:

```sql
CREATE DATABASE book_summarizer;
```

Then import the provided SQL dump:

```bash
mysql -u root -p book_summarizer < book_summarizer_dump.sql
```

### 6. Start Ollama

Run:

```bash
ollama serve
```

If required, download the configured model:

```bash
ollama pull llama3
```

### 7. Run the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

---

## 👤 Application Workflow

1. User registers or logs into the platform.
2. User uploads a PDF/TXT file or enters text directly.
3. The application extracts and preprocesses the content.
4. Large content is divided into smaller chunks.
5. Each chunk is processed using an LLM.
6. The chunk summaries are combined into a final summary.
7. The user selects the required summary length and format.
8. The generated summary can be regenerated, copied, or downloaded.
9. The processed content can also be used to generate:

   * Mind maps
   * Quizzes
   * AI chatbot responses
10. Relevant information is stored in the MySQL database.

---

## 🎓 Use Cases

Summarium can be useful for:

* Students studying lengthy textbooks
* Researchers reviewing documents
* Readers who want quick book insights
* Professionals processing large documents
* Revision and exam preparation
* Learning through AI-generated quizzes and mind maps

---

## 🚀 Future Enhancements

Possible future improvements include:

* 🌐 Multi-language summarization
* 🔎 RAG-based document retrieval
* 📷 OCR support for scanned PDFs
* 🎙️ Voice-based summarization
* 📱 Mobile application
* 📊 Personalized learning analytics

---

## 👩‍💻 Developed As

This project was developed as part of the **Infosys Springboard Virtual Internship**.

**Project:** Intelligent NLP System for Automated Book Summaries with Key Concept Identification

**Domain:** Natural Language Processing / Generative AI

---

## 📌 Project Highlights

* AI-powered document summarization
* Chunk-based processing for lengthy documents
* Multiple summary lengths and formats
* PDF/TXT/direct text input
* Mind-map generation
* AI-generated quizzes
* AI chatbot
* User authentication and authorization
* MySQL-based data management
* Admin dashboard
* FastAPI backend
* Groq and Ollama LLM integration
