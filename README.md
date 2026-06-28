# 🔥 Fireflies.ai Clone

A full-stack **Fireflies.ai-inspired meeting assistant** built with **Next.js**, **FastAPI**, and **SQLite**.

The application allows users to upload meeting transcripts, automatically extract participants, generate meeting summaries, identify key discussion topics, create action items, and browse previous meetings through a modern dashboard.

---

# 🚀 Features

## Dashboard

* View all meetings
* Responsive meeting cards
* Search meetings by title, summary, and key topics
* Modern Fireflies-inspired interface

## Meeting Details

Each meeting contains:

* 📝 AI-generated Summary
* 👥 Participants
* 📄 Transcript Viewer
* 🏷️ Key Topics
* ✅ Action Items
* ⏱️ Meeting Duration
* 📅 Meeting Date

## Transcript Upload

Supports:

* `.txt`
* `.md`

Uploading automatically:

* Creates a new meeting
* Extracts participants
* Generates summary
* Identifies key topics
* Extracts action items
* Creates transcript entries
* Redirects to the new meeting

## Action Items

* Automatically extracted using heuristic rules
* Can be marked complete
* Changes persist after refresh

---

# 🛠 Tech Stack

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Axios
* React Hot Toast
* Lucide React

## Backend

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn

---

# 📂 Project Structure

```
fireflies_clone
│
├── backend
│   ├── app
│   ├── meetings.db
│   ├── requirements.txt
│   └── seed.py
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── next.config.ts
│
└── README.md
```

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/<your-username>/fireflies-ai-clone.git

cd fireflies-ai-clone
```

---

## Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs on

```
http://localhost:8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:3000
```

---

# 📋 Sample Workflow

1. Start the backend server.
2. Start the frontend.
3. Open the dashboard.
4. Upload a `.txt` or `.md` transcript.
5. View the generated meeting.
6. Search meetings.
7. Open meeting details.
8. Mark action items as completed.

---

# ✨ Highlights

* Fireflies.ai-inspired dashboard
* Responsive UI
* Transcript upload
* Automatic participant extraction
* Automatic summary generation
* Automatic key topic extraction
* Automatic action item extraction
* Search functionality
* Persistent action item status
* Modern card-based design

---

# 🔮 Future Improvements

* Authentication
* Real AI summarization using LLMs
* Speech-to-text support
* Calendar integration
* Cloud database
* Team collaboration
* Role-based access
* Semantic search

---

# 📸 Screenshots

Add screenshots here before submission if required.

Example:

* Dashboard
* Meeting Details
* Upload Flow
* Transcript Viewer
* Action Items

---

# 👩‍💻 Author

**Shefali Ballal**

Final Year – Information Science & Engineering

B.M.S. College of Engineering

---

**Built as part of a Full-Stack Software Engineering assignment inspired by Fireflies.ai.**
