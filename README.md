# Intelligent NLP System for Automated Book Summaries with Key Concept Identification

An AI-powered web application that generates intelligent summaries from books and textual content using Natural Language Processing (NLP), Ollama, and Groq-powered Large Language Models (LLMs).

Developed as part of the **Infosys Springboard Virtual Internship (February 2026 – April 2026)**.

---

## 📌 Project Overview

Reading large books and documents can be time-consuming and overwhelming. This project addresses that challenge by providing an intelligent platform capable of generating concise and meaningful summaries while also offering interactive learning features such as quizzes, mind maps, and AI-powered assistance.

The system accepts PDF files, TXT files, or direct text input, processes the content through an NLP pipeline, and generates summaries in multiple formats and lengths according to user preferences.

---

## ✨ Features

### 🔐 Authentication & Authorization

* User Registration and Login
* Forgot Password using Security Questions
* Role-Based Access Control
* User Dashboard
* Admin Dashboard

### 📄 Multiple Input Methods

Users can provide content through:

* PDF Upload
* TXT File Upload
* Direct Text Input

Each submission generates a unique:

* Book ID
* Text ID

---

### 🤖 AI-Powered Summarization

Generate summaries in:

#### Formats

* Bullet Points
* Paragraph Format

#### Lengths

* Short
* Medium
* Detailed

Additional Features:

* Unlimited Summary Regeneration
* Summary History
* PDF Download
* Copy to Clipboard

---

### 🧠 Mind Map Generation

The system automatically extracts key concepts and generates visual mind maps.

Features:

* Concept Extraction
* Relationship Mapping
* JPG Export Support

---

### ❓ Quiz Generation

Automatically generates quizzes from summarized content.

Features:

* AI-Generated Questions
* Automatic Evaluation
* Score Calculation
* Incorrect Answer Identification
* Correct Answer Display

---


### 📚 Uploaded Books Repository

Centralized repository of uploaded books.

Features:

* Book ID Tracking
* Book Name & Author Storage
* Search Functionality
* Duplicate Upload Prevention

---

### 👨‍💼 Admin Dashboard

Administrators can:

* View Users
* View Uploaded Books
* Monitor Summary Statistics
* Delete Users
* Delete Books
* Manage Platform Data

---

## ⚙️ NLP Processing Pipeline

```text
Input Content
      ↓
Text Extraction
      ↓
Text Preprocessing
      ↓
Chunking
      ↓
Chunk Summarization
      ↓
Final Summary Generation
      ↓
Storage in Database
      ↓
Quiz / Mind Map / Chatbot
```

### Text Preprocessing

* Cleaning and normalization
* Removal of unwanted characters
* Formatting correction
* Content validation

### Text Chunking

Large documents are divided into manageable chunks before processing to overcome LLM token limitations.

### Chunk Summarization

Each chunk is summarized independently and stored for later processing.

### Final Summary Generation

Chunk summaries are combined and refined to generate the final coherent summary.

---

## 🏗️ System Architecture

```text
User
  │
  ▼
PDF / TXT Upload / Text Input
  │
  ▼
Text Extraction
  │
  ▼
NLP Preprocessing
  │
  ▼
Chunking Engine
  │
  ▼
Ollama + Groq API
  │
  ▼
Summary Generation
  │
  ├── Mind Map Generator
  ├── Quiz Generator
  └── AI Chatbot
  │
  ▼
MySQL Database
```

---

## 🛠️ Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* FastAPI
* Uvicorn

### Database

* MySQL

### AI & NLP

* Ollama
* Groq API
* NLP Text Processing
* Chunk-Based Summarization
* Large Language Models (LLMs)

---

## 🗄️ Database Structure

### users

Stores user account information.

| Field      | Description            |
| ---------- | ---------------------- |
| user_id    | Primary Key            |
| name       | User Name              |
| email      | Email Address          |
| password   | Encrypted Password     |
| role       | User/Admin             |
| created_at | Registration Timestamp |

### books

Stores uploaded book metadata.

| Field       | Description      |
| ----------- | ---------------- |
| book_id     | Primary Key      |
| title       | Book Title       |
| author      | Author Name      |
| uploaded_by | User Reference   |
| upload_date | Upload Timestamp |

### raw_text

Stores extracted text content.

### pasted_texts

Stores manually entered text.

### chunk_summaries

Stores intermediate summaries generated during chunk processing.

### summaries

Stores final generated summaries.

---

## 🚀 Installation

### Prerequisites

Install:

* Python 3.10+
* MySQL
* Ollama

---

### Clone Repository

```bash
git clone https://github.com/yourusername/intelligent-book-summarizer.git

cd intelligent-book-summarizer
```

---

### Create Virtual Environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=book_summarizer

GROQ_API_KEY=your_groq_api_key

OLLAMA_MODEL=llama3
```

---

### Database Setup

Create database:

```sql
CREATE DATABASE book_summarizer;
```

Import schema:

```bash
mysql -u root -p book_summarizer < database.sql
```

---

### Start Ollama

```bash
ollama serve
```

Pull model if required:

```bash
ollama pull llama3
```

---

## ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

Open in browser:

```text
http://localhost:8000
```

---

## 📋 Application Workflow

1. User logs in.
2. Uploads PDF/TXT file or pastes text.
3. Book ID or Text ID is generated.
4. Content is stored and processed.
5. User enters the generated ID in the summarization section.
6. User selects:

   * Summary Format
   * Summary Length
7. AI generates summary.
8. User can:

   * Regenerate Summary
   * Download PDF
   * Copy to Clipboard
   * View History
9. Additional modules:

   * Mind Map Generation
   * Quiz Generation
   * AI Chatbot
   * Uploaded Books Repository

---

## 🔮 Future Enhancements

* Multi-Language Summarization
* OCR Support for Scanned PDFs
* Voice-Based Summarization
* RAG-Based Retrieval System
* Mobile Application
* Personalized Learning Analytics

