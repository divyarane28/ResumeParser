# 📄 AI Resume Parser & Job Description Matcher

An AI-powered web application that extracts structured candidate information from PDF resumes and analyzes how well a resume matches a given Job Description (JD).

The application uses **FastAPI, PyMuPDF, Hugging Face Inference API, and Meta Llama 3.1 8B Instruct** to parse resumes, analyze job descriptions, and perform semantic skill matching.

---

## 🚀 Features

### 📄 Resume Parsing

* Upload Resume in PDF format
* Extract resume text using PyMuPDF
* AI-powered resume information extraction
* Automatic extraction of:

  * Name
  * Email
  * Phone
  * Skills
  * Education
  * Experience
* Auto-fill editable candidate profile
* Manual editing support
* Candidate profile page

### 💼 Job Description Analysis

* Paste a Job Description
* Extract important JD requirements using LLM
* Identify:

  * Required Skills
  * Preferred Skills
  * Experience Requirements
  * Education Requirements

### 📊 Resume-JD Matching

* Compare the resume against the Job Description
* Perform semantic skill matching using LLM
* Analyze skills from the broader resume content rather than relying only on the extracted Skills section
* Identify:

  * Matching Required Skills
  * Missing Required Skills
  * Matching Preferred Skills
  * Version mismatches
* Calculate an overall **Resume Match Percentage**
* Handle semantically equivalent skill names such as:

  * `Excel` ↔ `Microsoft Excel`
  * `Power BI` ↔ `PowerBI`
  * `VLOOKUP/XLOOKUP` ↔ `VLOOKUP` + `XLOOKUP`
* Distinguish between similar but different technologies such as `C`, `C#`, and `CSS`

---

## 🧠 AI Matching Approach

The application uses an LLM to understand the context of skills and determine whether a candidate's resume provides evidence of a required skill.

The matching process considers information from:

* Skills
* Work experience
* Technical responsibilities
* Projects
* Other relevant resume content

The LLM performs the semantic analysis, while Python processes the result and calculates the final match percentage.

This approach helps avoid relying only on exact keyword matching.

---

## 🛠 Tech Stack

* **Python**
* **FastAPI**
* **Hugging Face Inference API**
* **Meta Llama 3.1 8B Instruct**
* **PyMuPDF**
* **HTML**
* **CSS**
* **JavaScript**

---

## 📂 Project Structure

```text
AI-Resume-Parser/
│
├── .env                         # Hugging Face API Key
├── .gitignore                   # Ignore .env, uploads, __pycache__
├── README.md                    # Project Documentation
├── requirements.txt             # Python Packages
│
├── main.py                      # FastAPI Application & API Routes
├── parser.py                    # PDF Text Extraction
├── llm_service.py               # Hugging Face LLM Integration
├── matcher.py                   # Resume-JD Matching Logic
│
├── uploads/                     # Uploaded Resume PDFs
│
├── templates/
│      ├── index.html            # Resume Upload + JD Matching Interface
│      └── candidate.html        # Candidate Profile Page
│
├── static/
│      ├── style.css             # Common CSS
│      ├── script.js             # index.html JavaScript
│      └── candidate.js          # candidate.html JavaScript
│
├── sample_resume.txt            # Sample Resume (Testing)
├── test.py                      # Resume Parsing Testing
├── test_hf.py                   # Hugging Face Testing
└── check_import.py              # Import Testing
```

---

## ⚙️ Application Workflow

```text
                    Resume PDF
                        │
                        ▼
                  PyMuPDF
                Text Extraction
                        │
                        ▼
              Hugging Face LLM
              Resume Information
                  Extraction
                        │
                        ▼
              Structured Resume JSON
                        │
                        │
                        ▼
                 Candidate Profile
                        
                        
Job Description ────────┐
                        ▼
                Hugging Face LLM
                  JD Analysis
                        │
                        ▼
              Required / Preferred
                    Skills
                        │
                        ▼
             Resume + JD Matching
                        │
                        ▼
              Semantic Skill Analysis
                        │
                        ▼
              Python Match Calculation
                        │
                        ▼
              Resume Match Percentage
                        │
                        ▼
       ┌────────────────────────────────┐
       │ Matching Required Skills       │
       │ Missing Required Skills        │
       │ Matching Preferred Skills      │
       │ Version Mismatches             │
       └────────────────────────────────┘
```

---

## 📌 AI Workflow

### 1. Resume Upload

The user uploads a PDF resume through the web interface.

### 2. Text Extraction

PyMuPDF extracts the text from the uploaded PDF.

### 3. Resume Parsing

The extracted resume text is sent to the **Meta Llama 3.1 8B Instruct** model through the Hugging Face Inference API.

The LLM converts the unstructured resume into structured JSON containing candidate information.

### 4. Job Description Analysis

The user pastes a Job Description.

The LLM analyzes the JD and extracts:

* Required skills
* Preferred skills
* Experience requirements
* Education requirements

### 5. Semantic Matching

The resume and analyzed JD are provided to the matching process.

The LLM evaluates whether each JD skill is supported by the candidate's resume based on semantic and contextual evidence.

### 6. Match Calculation

Python processes the LLM's skill analysis and calculates the overall match percentage based on the required skills.

```text
Match Percentage =
Matched Required Skills
------------------------ × 100
Total Required Skills
```

### 7. Match Result

The application displays:

* Resume Match %
* Matching Required Skills
* Missing Required Skills
* Matching Preferred Skills
* Version Mismatches

---

## 📊 Example Match Result

```json
{
  "match_percentage": 71.43,
  "matched_required_skills": [
    "SQL",
    "Microsoft Excel",
    "Power BI",
    "Pivot Tables",
    "Power Query"
  ],
  "missing_required_skills": [
    "VBA"
  ],
  "matched_preferred_skills": [
    "Python",
    "Pandas",
    "DAX"
  ],
  "version_mismatches": []
}
```

The percentage is calculated using the **required skills**, while preferred skills are displayed separately.

---

## 🔍 Semantic Skill Matching

The application is designed to understand that different representations can refer to the same skill.

For example:

```text
JD                         Resume
------------------------------------------------
Microsoft Excel       →    Excel
Power BI              →    PowerBI
VLOOKUP/XLOOKUP       →    VLOOKUP + XLOOKUP
Python                →    Python 3.x
```

The matcher also attempts to avoid incorrect matches between technologies that have similar names:

```text
C       ≠ C#
C       ≠ CSS
Python  ≠ PyTorch
```

The goal is to evaluate the **meaning and context of the skill**, rather than simply searching for an exact keyword.

---

## 🧪 Testing

The application can be tested using different combinations of resumes and Job Descriptions.

Example:

```text
Data Analyst Resume
        +
Data Analyst JD
        ↓
Higher Match Percentage
```

```text
Non-Data Analyst Resume
        +
Data Analyst JD
        ↓
Lower Match Percentage
        +
Missing Required Skills
```

This helps evaluate the semantic matching behavior of the application.

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
HF_API_KEY=your_huggingface_api_key
```

The `.env` file should not be committed to GitHub.

Add it to `.gitignore`:

```text
.env
uploads/
__pycache__/
.venv/
```

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
  ],
  "education": [
    "Bachelor of Computer Science"
  ],
  "experience": [
    "Data Analyst - ABC Company"
  ]
}
```

---

## 📱 LinkedIn

I shared a short demo and details about this project on LinkedIn:

[LinkedIn Project Post](https://lnkd.in/p/ddce5X9H?utm_source=chatgpt.com)

---

## 👩‍💻 Author

**Divya Rane**

https://www.linkedin.com/in/divya-rane-a26254326
