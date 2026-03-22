🌿 LCEL Study Buddy
An AI-powered study assistant I built using LangChain Expression Language (LCEL), Gemini 2.5 Flash, FastAPI, and Streamlit.

🎯 What It Does
You paste your study notes (or upload a PDF), and the app:

1) Analyzes your notes using Gemini and finds the 3 topics you're most likely to struggle with
2) Generates a personalized multiple choice quiz based on those weak spots
3) Lets you click A/B/C/D answers interactively — no typing needed
4) Grades your answers instantly and shows your score with feedback
5) Gives you personalized study tips targeting your exact weak topics

🗂️ Project Structure

lcel-study-buddy/
├── main.py  
│          
├── app.py
│           
├── requirements.txt
├── .env                 
├── .gitignore
└── README.md

⚙️ Setup & Installation

1. Clone the repo

2. Install dependencies

3. Add your API key
Create a .env file in the root folder:
GOOGLE_API_KEY=your_gemini_api_key_here

4. Run the backend (Terminal 1)
uvicorn main:app --reload --port 8000

5. Run the frontend (Terminal 2)
streamlit run app.py

6. Open in browser

