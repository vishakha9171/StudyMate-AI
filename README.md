# StudyMate-AI
StudyMate AI — An AI-powered study assistant that answers questions strictly from uploaded course materials, provides precise page-level citations, understands handwritten notes, and refuses unsupported questions.


<div align="center">

# 📚 StudyMate AI

### Your Course Material. One Intelligent Study Assistant.

**Ask questions from PDFs, presentations, and handwritten notes — and get grounded answers with source references.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#license)

</div>

---

## ✨ Overview

**StudyMate AI** is an AI-powered course material assistant designed to help students understand and navigate their study material faster.

Instead of manually searching through dozens of pages of notes and presentations, students can simply upload their material and ask questions in natural language.

StudyMate AI can work with:

- 📄 PDF documents
- 📊 PowerPoint presentations
- ✍️ Handwritten notes
- 💬 Natural-language questions

The core idea is simple:

> **Your study material should be the source of truth.**

StudyMate AI therefore focuses on generating answers grounded in the uploaded material and avoids confidently answering questions when the required information is not present.

---

# 🎯 Why StudyMate AI?

Students often have their study material spread across:

- Lecture PDFs
- PPT presentations
- Scanned notes
- Handwritten notebooks
- Multiple course documents

Finding one specific piece of information can take several minutes.

StudyMate AI turns this workflow into:

```text
Upload → Ask → Understand → Verify


                    ┌─────────────────────┐
                    │       Student       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │                     │
                    │ Upload + Q&A UI     │
                    └──────────┬──────────┘
                               │
                         HTTP / API
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
               ┌───────────────┼────────────────┐
               │               │                │
               ▼               ▼                ▼
          PDF Parser      PPT Parser      Image / OCR
               │               │                │
               └───────────────┼────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Material Context  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Gemini AI        │
                    │   Question Analysis │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Grounded Response   │
                    │ + Source Reference  │
                    └─────────────────────┘