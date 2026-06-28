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
git clone https://github.com/shefaliballal/fireflies_clone.git

cd fireflies_clone
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

# 📸 Screenshots and video recordings

Video link: https://drive.google.com/file/d/1qcjKfU0jEmiK3Hd2qF5UGma5unXu7j64/view?usp=sharing


<p align="center">
  <img src="https://github.com/user-attachments/assets/cb9cfcef-0151-4ef4-afa5-e8ddc6dcdcc1" width="700">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/6f55f6e5-1190-41c8-8274-c0505406a871" width="700">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e1aa7078-4625-44c7-856d-ef5ba302d583" width="700">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/82100a6a-7f45-4218-9d65-8cfc412d366b" width="700">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3f6b5d7b-8757-48db-adc2-eee5ec9ac453" width="700">
</p>

---

# 👩‍💻 Author

**Shefali Ballal**


B.M.S. College of Engineering


