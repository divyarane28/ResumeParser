# ResumeParser# 📄 AI Resume Parser using FastAPI & Hugging Face LLM

An AI-powered Resume Parser that automatically extracts candidate information from PDF resumes using Large Language Models (LLMs).

The application converts unstructured resume content into structured JSON and auto-fills an editable candidate profile.

---

## 🚀 Features

- Upload Resume (PDF)
- Extract text using PyMuPDF
- AI-powered information extraction using Hugging Face LLM
- Automatic extraction of:
  - Name
  - Email
  - Phone
  - Skills
  - Education
  - Experience
- Auto-fill editable candidate form
- Manual editing support
- Candidate profile page
- Responsive web interface

---

## 🛠 Tech Stack

- Python
- FastAPI
- Hugging Face Inference API
- Meta Llama 3.1 8B Instruct
- PyMuPDF
- HTML
- CSS
- JavaScript

---

## 📂 Project Structure

AI-Resume-Parser/
│
├── .env                         # Hugging Face API Key
├── .gitignore                   # Ignore .env, uploads, __pycache__
├── README.md                    # Project Documentation
├── requirements.txt             # Python Packages
│
├── main.py                      # FastAPI Application & Routes
├── parser.py                    # PDF Text Extraction
├── llm_service.py               # Hugging Face LLM Integration
│
├── uploads/                     # Uploaded Resume PDFs
│      ├── resume1.pdf
│      └── ....
│
├── templates/
│      ├── index.html            # Upload + Auto-fill Candidate Form
│      └── candidate.html        # Candidate Profile Page
│
├── static/
│      ├── style.css             # Common CSS
│      ├── script.js             # index.html JavaScript
│      └── candidate.js          # candidate.html JavaScript
│
│
├── sample_resume.txt            # Sample Resume (Testing)
├── test.py                      # parse_resume() Testing
├── test_hf.py                   # Hugging Face Testing
└── check_import.py              # Import Testing (Optional)

## ⚙️ Workflow

```
Resume PDF
      │
      ▼
PyMuPDF
(Text Extraction)
      │
      ▼
Hugging Face LLM
      │
      ▼
Structured JSON
      │
      ▼
Auto-filled Candidate Form
      │
      ▼
Candidate Profile
```

---

## 📌 AI Workflow

1. User uploads a PDF resume.
2. PyMuPDF extracts text from the document.
3. The extracted text is sent to the Hugging Face LLM.
4. The LLM understands the resume and converts it into structured JSON.
5. The JSON response automatically populates the candidate profile form.
6. Users can review and edit the extracted information before saving.

---

## 💡 Sample Extracted Information

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "skills": [
    "Python",
    "SQL",
    "FastAPI",
    "Power BI"
  ]
}
```

---


## Author

**Divya Rane**

LinkedIn: linkedin.com/in/divya-rane-a26254326
