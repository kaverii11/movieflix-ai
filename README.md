# 🎬 Movieflix AI - Intelligent Movie Recommender

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movieflix-ai.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Machine Learning](https://img.shields.io/badge/AI-Sentence%20Transformers-orange)
![API](https://img.shields.io/badge/API-TMDB-green)

**Movieflix AI** is a content-based recommendation engine that suggests movies based on semantic similarity. Unlike simple keyword matching, it uses **Deep Learning (BERT models)** to understand the *meaning* behind movie plots, genres, and tags.

🔴 **Live Demo:** [Click here to view the App](https://movieflix-ai.streamlit.app/)

---

## 📸 Screenshots

| Home Page | Recommendations |
|:---:|:---:|
| <img width="440" height="900" src="https://github.com/user-attachments/assets/3df940d1-dde3-460b-bbb8-43e17ee8b575" />
" | <img width="1436" height="654" alt="Screenshot 2025-12-23 at 16 01 22" src="https://github.com/user-attachments/assets/adb6bb13-37eb-4557-85d2-70371d5af7a6" /> |
---

## 🧠 How It Works (The "Brain")

1.  **Data Processing:** * The system uses the **TMDB 5000 Movie Dataset**.
    * It combines `Overview`, `Genres`, `Keywords`, `Cast`, and `Crew` into a single "tag" for each movie.

2.  **Vectorization (The Upgrade):**
    * Instead of a basic "Bag of Words" model, this project uses **SBERT (Sentence-BERT)**.
    * Specifically, the `all-MiniLM-L6-v2` model transforms text into high-dimensional vectors (384 dimensions), capturing semantic meaning (e.g., understanding that "Space War" is similar to "Alien Invasion").

3.  **Similarity:**
    * We calculate the **Cosine Similarity** between these vectors to find movies that are mathematically closest to the user's choice.

4.  **Frontend & API:**
    * **Streamlit** powers the interactive UI.
    * **TMDB API** dynamically fetches high-quality movie posters.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Language:** Python
* **Machine Learning:** Scikit-Learn, Sentence-Transformers (BERT)
* **Data Manipulation:** Pandas, NumPy
* **API:** The Movie Database (TMDB)
