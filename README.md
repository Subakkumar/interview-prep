# Interview Prep Assistant

AI-powered coding interview practice platform. Practice real problems, get progressive hints, and receive detailed AI feedback on your solutions.

## Features

- 10 problems across Easy / Medium categories
- Progressive hints — 3 levels, each more specific
- Live test runner — run code against hidden test cases
- AI evaluation — time complexity, score, specific improvement tips
- Attempt history per problem

## Tech Stack

- **Backend** — Python, Flask, SQLAlchemy, SQLite
- **AI** — Groq API (Llama 3.3 70B)
- **Code Runner** — Python AST + exec sandbox
- **Frontend** — Vanilla JS, custom CSS

## Setup

1. Clone the repo
2. `python -m venv venv` → activate
3. `pip install -r requirements.txt`
4. Add `GROQ_API_KEY=your_key` to `.env`
5. `python seed_problems.py` — load all problems
6. `python app.py`
7. Open `http://localhost:5009`

## Problems Included

Arrays, Strings, Stacks, Dynamic Programming, Binary Search, Graphs, Linked Lists, Recursion

## Screenshots

<img width="1919" height="1024" alt="image" src="https://github.com/user-attachments/assets/8a26a2e6-5160-440e-b59d-b1660bab0540" />
<img width="1919" height="1024" alt="image" src="https://github.com/user-attachments/assets/c7cd9a97-0070-4d8f-a5e9-92c3e8b6e6a5" />
