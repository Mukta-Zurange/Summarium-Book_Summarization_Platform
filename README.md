# 📚 Summarium – AI-Powered Book & Content Summarization Platform

**Summarium** is an AI-powered content summarization platform designed to help users quickly understand books, documents, text, and YouTube videos without reading or watching the entire source.

The platform uses **Natural Language Processing (NLP)** and **Large Language Models (LLMs)** to extract important information, generate personalized summaries, identify key insights, and provide interactive learning tools such as mind maps, quizzes, and an AI chatbot.

---

## 🎯 Project Objective

Reading lengthy books, documents, research material, and watching long educational videos can be time-consuming when users only need the most important information.

Summarium solves this problem by processing large amounts of content and transforming it into concise, meaningful, and user-oriented summaries. Users can control the **summary format, length, and target audience/role**, making the generated content more relevant to their specific needs.

The platform also provides **key insights, mind maps, quizzes, chatbot interaction, summary history, and PDF export**, making it useful for learning, research, revision, and professional information processing.

---

## ✨ Key Features

### 🔐 User Authentication

* User registration and login
* Secure password handling
* Password recovery using security questions
* Role-based access control
* Separate user and administrator functionality

---

### 📄 Multiple Content Input Methods

Summarium supports multiple ways of providing content:

* 📕 **PDF Upload**
* 📄 **TXT File Upload**
* 📝 **Direct Text Input**
* ▶️ **YouTube Video Link**

For YouTube videos, Summarium extracts the available transcript and converts it into processable text before sending it through the summarization pipeline.

The platform validates YouTube URLs and handles cases such as unavailable or disabled transcripts.

---

## 🤖 AI-Powered Summarization

Summarium uses an LLM-powered summarization pipeline to generate summaries from large amounts of content.

Users can customize the generated summary according to their requirements.

### Summary Formats

* **Paragraph**
* **Bullet Points**

### Summary Lengths

* **Short**
* **Medium**
* **Detailed**

### Role-Based Summarization

A major feature of Summarium is the ability to generate summaries specifically for different types of users.

Available roles include:

| Role           | Summary Focus                                                   |
| -------------- | --------------------------------------------------------------- |
| 🌐 General     | Balanced summary of the content                                 |
| 🎓 Student     | Simple explanations and important concepts                      |
| 💼 Executive   | Decisions, outcomes, business impact and actionable information |
| 💻 Technical   | Technical details, methods and terminology                      |
| 🔬 Researcher  | Methodology, findings, evidence and implications                |
| ⚖️ Legal       | Rights, obligations, risks and legal implications               |
| 🎨 Creative    | Engaging explanations, analogies and storytelling               |
| 🩺 Medical     | Clinical details, treatments and outcomes                       |
| 📊 Analyst     | Metrics, trends, patterns and data-driven conclusions           |
| 👨‍🏫 Educator    | Learning objectives and concepts useful for teaching            |

The selected role is incorporated into the LLM prompt so that the final summary is adapted to the intended audience.

---

## 🔄 Summary Controls

Summarium provides several controls to make the summarization experience more flexible:

* ▶️ **Generate Summary** – Creates a new summary from the processed content
* 🔄 **Regenerate** – Generates another version of the summary
* ⏳ **History** – Access previously generated summaries
* 📋 **Copy** – Copies the generated summary to the clipboard
* 📥 **Download PDF** – Downloads the summary as a PDF document

The system also stores summaries and chunk-level results in the MySQL database, allowing previously processed information to be reused efficiently.

---

## 💡 AI-Powered Key Insights

Summarium can extract the most important takeaways from a generated summary using the **Key Insights** feature.

The system:

1. Takes the generated summary as input.
2. Sends it to the LLM for analysis.
3. Identifies the most important takeaways.
4. Generates **five concise key insights**.
5. Displays the insights separately for quick understanding.

This allows users to understand the core message of lengthy content without reading the complete summary.

---

## 🧠 Mind Map Generation

Summarium can convert summarized content into a structured visual mind map.

The AI analyzes the content and determines the most suitable structure, such as:

* General concepts
* Step-by-step processes
* Hierarchies and classifications
* Comparisons
* Cause-and-effect relationships
* Timelines

The generated structure contains a central topic, main concepts, and supporting details.

This feature helps users visually understand relationships between important concepts.

---

## ❓ AI Quiz Generation

Summarium can generate quizzes from processed content.

The quiz system provides:

* AI-generated questions
* Multiple-choice options
* Difficulty levels
* Automatic answer evaluation
* Score calculation
* Identification of incorrect answers
* Correct answer explanations

This makes the platform useful for **self-assessment, exam preparation, and revision**.

---

## 💬 AI Chatbot

Users can interact with an AI-powered chatbot to ask questions related to their processed content.

The chatbot can:

* Answer questions about the content
* Explain concepts
* Provide additional clarification
* Maintain conversation history
* Generate context-related responses

This allows users to interact with their learning material rather than simply reading a static summary.

---

## 📚 Content & Summary History

Summarium maintains a history of processed content and generated summaries.

Users can revisit previously processed:

* Books
* Uploaded documents
* Directly entered text
* YouTube transcripts

The history system stores information such as the content title, summary type, and creation date.

---

## 👨‍💼 Admin Dashboard

Administrators have dedicated functionality for monitoring and managing the platform.

The admin dashboard provides:

* 👥 User management
* 📚 Book management
* 📊 Summary statistics
* 🔎 Content monitoring
* 🗑️ Book deletion
* 📈 Summary information

This provides centralized control over the application.

---

# 🔄 System Workflow

```text
                         USER
                           │
                           ▼
              ┌─────────────────────────┐
              │     Content Input       │
              ├─────────────────────────┤
              │ PDF                     │
              │ TXT                     │
              │ Direct Text             │
              │ YouTube Link            │
              └────────────┬────────────┘
                           │
                           ▼
                  Content Extraction
                           │
                           ▼
                   Text Preprocessing
                           │
                           ▼
                       Chunking
                           │
                           ▼
                 Chunk Summarization
                           │
                           ▼
              Role + Length + Format
                     Customization
                           │
                           ▼
                 Final AI Summary
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        Key Insights    Mind Map       Quiz
              │
              ▼
         AI Chatbot
              │
              ▼
          MySQL Database
              │
              ▼
      History / PDF / Copy
```

---

# 🧠 NLP & AI Summarization Pipeline

Large documents cannot always be processed by an LLM in a single request because of context and token limitations.

Therefore, Summarium uses a **chunk-based summarization approach**.

### 1. Content Extraction

Content is extracted from:

* PDF files
* TXT files
* Direct text
* YouTube transcripts

For YouTube content, the application extracts the video's transcript and converts it into text for further processing.

### 2. Text Preprocessing

The extracted text is cleaned and normalized before summarization.

This includes:

* Removing unwanted formatting
* Cleaning text
* Normalizing content
* Validating extracted information

### 3. Text Chunking

Large documents are divided into smaller chunks.

This prevents large inputs from exceeding the context limitations of the language model.

### 4. Chunk-Level Summarization

Each chunk is processed independently using the configured LLM.

The resulting chunk summaries are stored and can be reused during later summary generation.

### 5. Final Summary Generation

The chunk summaries are combined and passed to the LLM again.

The final output is generated according to the user's:

* Summary format
* Summary length
* Selected role

This allows the same source material to produce different summaries for different audiences.

### 6. Additional AI Processing

The final summary can then be used for:

* 💡 Key insights
* 🧠 Mind maps
* ❓ Quizzes
* 💬 AI chatbot interaction

---

# 🏗️ Technology Stack

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
* Groq API
* `openai/gpt-oss-20b`
* Chunk-based summarization
* Prompt-based role customization

### Database

* MySQL
* SQLAlchemy

### Content Processing

* PDF/Text extraction
* YouTube Transcript API
* Text preprocessing
* Custom chunking pipeline

### Configuration

* Python `.env`
* Environment variables

---

# 📁 Project Structure

```text
Summarium-Book_Summarization_Platform/
│
├── static/
│   ├── CSS
│   ├── JavaScript
│   └── Frontend assets
│
├── templates/
│   └── HTML templates
│
├── app.py
│   └── Main FastAPI application and API endpoints
│
├── auth_utils.py
│   └── Authentication and authorization utilities
│
├── database.py
│   └── MySQL database connection and operations
│
├── models.py
│   └── SQLAlchemy database models
│
├── extractor.py
│   └── Content extraction logic
│
├── preprocessing.py
│   └── Text preprocessing and cleaning
│
├── summarizer.py
│   └── AI summarization and LLM logic
│
├── utils.py
│   └── Supporting utility functions
│
├── requirements.txt
│   └── Python dependencies
│
├── .env.example
│   └── Environment variable template
│
└── README.md
    └── Project documentation
```

The current repository contains the FastAPI application, authentication utilities, database layer, extraction/preprocessing modules, summarization logic, frontend assets, and environment configuration.

---

# 🗄️ Database

Summarium uses **MySQL** to store application and summarization data.

The database manages information related to:

* Users
* Books
* Uploaded content
* Pasted text
* Extracted text
* Chunk summaries
* Final summaries
* Summary history
* Chat messages


The database allows the application to maintain user data, uploaded content, generated summaries, and historical results.

---

# ⚙️ Installation & Setup

## Prerequisites

Make sure the following are installed:

* Python 3.10+
* MySQL
* Git

You will also need a **Groq API key** for the LLM-powered features.

---

## 1. Clone the Repository

```bash
git clone https://github.com/Mukta-Zurange/Summarium-Book_Summarization_Platform.git

cd Summarium-Book_Summarization_Platform
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=book_summarizer

GROQ_API_KEY=your_groq_api_key
```

Do not commit your actual `.env` file or API keys to GitHub.

---

## 5. Configure MySQL

Create the database:

```sql
CREATE DATABASE book_summarizer;
```


If you are using a cloud MySQL provider, configure the corresponding host, username, password, database name, and port in `.env`.

---

## 6. Run the Application

Start the FastAPI application:

```bash
uvicorn app:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

---

# 👤 Application Workflow

1. User registers or logs into Summarium.
2. User selects a content input method.
3. User uploads a PDF/TXT file, enters text, or provides a YouTube link.
4. The application extracts the content.
5. The text is cleaned and preprocessed.
6. Large content is divided into manageable chunks.
7. Chunk-level summaries are generated.
8. The chunks are combined into a final summary.
9. The user selects:

   * Summary length
   * Summary format
   * Target role
10. The final personalized summary is generated.
11. The user can:

* Regenerate the summary
* View history
* Copy the summary
* Download it as PDF

12. The user can generate **Key Insights**.
13. The processed content can also be used for:

* Mind maps
* Quizzes
* AI chatbot interaction

14. Relevant application data is stored in MySQL.

---

# 🎓 Use Cases

Summarium can be useful for:

* 🎓 Students studying lengthy textbooks
* 🔬 Researchers reviewing academic material
* 📚 Readers who want quick book summaries
* 💼 Professionals reviewing business documents
* 👨‍💻 Technical professionals analyzing technical content
* 👨‍🏫 Educators preparing teaching material
* 📝 Exam and revision preparation
* ▶️ Users who want quick insights from educational YouTube videos
* 📊 Professionals who need concise, role-specific information

---

# 🚀 Future Enhancements

Potential future improvements include:

* 🌐 Multilingual summarization
* 🔎 RAG-based document retrieval
* 📷 OCR support for scanned PDFs
* 🎙️ Voice-based summarization
* 📱 Mobile application
* 📊 Personalized learning analytics
* 🔗 Support for additional web content sources
* 🧠 More advanced personalization and recommendation features

---

# 🎓 Project Information

**Project:** Intelligent NLP System for Automated Book Summaries with Key Concept Identification

**Project Name:** Summarium

**Domain:** Natural Language Processing / Generative AI

**Developed As:** Infosys Springboard Virtual Internship Project

---

# 📌 Project Highlights

* 🤖 AI-powered content summarization
* 📚 Book and document summarization
* ▶️ YouTube transcript summarization
* 🎯 Role-based personalized summaries
* 📏 Multiple summary lengths
* 📝 Paragraph and bullet-point formats
* 🔄 Summary regeneration
* ⏳ Summary history
* 💡 AI-generated key insights
* 📋 One-click summary copying
* 📥 PDF summary download
* 🧠 AI-generated mind maps
* ❓ AI-generated quizzes
* 💬 Context-aware AI chatbot
* 🔐 User authentication and authorization
* 👨‍💼 Admin dashboard
* 🗄️ MySQL database
* ⚡ FastAPI backend
* 🧠 Groq LLM integration
* ✂️ Chunk-based processing for large documents

---

## 🌟 Why Summarium?

Summarium is more than a basic text summarizer.

It combines **AI summarization, audience personalization, content extraction, learning tools, and persistent history** into a single platform. Instead of simply producing a shorter version of a document, it allows users to choose **how the information should be presented and for whom it should be optimized**.

Whether the user is a student learning a new concept, a researcher reviewing a paper, an executive looking for business impact, or a professional analyzing technical material, Summarium adapts the generated summary to the user's needs.
