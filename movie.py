import streamlit as st
import pickle
import pandas as pd
import requests
import os
import urllib.parse
import time
import random

# 1. Setup Paths & Load Data
current_path = os.path.dirname(os.path.abspath(__file__))
dict_file_path = os.path.join(current_path, 'movie_dict.pkl')
similarity_file_path = os.path.join(current_path, 'similarity.pkl')

movies_dict = pickle.load(open(dict_file_path, 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(similarity_file_path, 'rb'))

# --- QUIRKY LOADING MESSAGES ---
loading_messages = [
    "Opening the secret vault...",
    "Wait for it... wait for it...",
    "Don't forget the snacks! 🍫",
    "Reading the scripts (skipping the boring parts)...",
    "The suspense is killing me...",
    "Dimming the lights... 💡",
    "Grab a blanket! 🛋️",
    "Microwaving the popcorn... 🍿",
    "Auditioning recommended movies..."
]

# --- CACHED POSTER FUNCTION (Silent Mode) ---
# show_spinner=False hides the "Running fetch_poster..." text
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id, title):

    api_key = "1d2875cfd1cc5ad4203156560555c9b3"
    
    safe_title = urllib.parse.quote(title)
    placeholder_url = f"https://placehold.co/500x750/222222/FFFFFF/png?text={safe_title}"

    for attempt in range(3):
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return "https://image.tmdb.org/t/p/w500/" + poster_path
                else:
                    return placeholder_url
            
            if response.status_code == 429:
                time.sleep(1)
                continue
                
        except Exception as e:
            time.sleep(1)
            continue
            
    return placeholder_url

# 2. Recommendation Logic
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_posters = []
        
        for i in movies_list:
            movie_id = movies.iloc[i[0]].id
            movie_title = movies.iloc[i[0]].title
            
            recommended_movies.append(movie_title)
            recommended_posters.append(fetch_poster(movie_id, movie_title))
            
        return recommended_movies, recommended_posters
    except Exception as e:
        return [], []

# 3. CSS Styling (Centered Title)
st.markdown("""
    <style>
        .stApp { background-color: #141414; color: white; }
        .stButton>button {
            background-color: #e50914; color: white; border-radius: 4px; border: none; font-weight: bold; width: 100%;
        }
        .stButton>button:hover {
            background-color: #b20710; color: white;
        }
        /* Custom Spinner Color */
        .stSpinner > div > div {
            color: #e50914 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 4. App Layout (Centered)
st.markdown("<h1 style='text-align: center; color: white;'>🎬 Movieflix AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #a1a1a1;'>Your Personal Movie Recommendation System</h3>", unsafe_allow_html=True)

st.write("") # Spacer

# Initialize session state
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# --- SEARCH BAR ---
search_query = st.selectbox(
    'Search for a movie:',
    movies['title'].values,
    index=None,
    placeholder="Type to search..."
)

if st.button('Show Recommendations'):
    if search_query:
        st.session_state.selected_movie = search_query
        
        # Pick a random quirky message
        random_message = random.choice(loading_messages)
        
        with st.spinner(random_message):
            names, posters = recommend(search_query)
        
        if names:
            st.markdown(f"### Because you watched **{search_query}**:")
            cols = st.columns(5)
            for col, name, poster in zip(cols, names, posters):
                with col:
                    st.image(poster, use_container_width=True)
                    st.caption(name)
        else:
            st.error("No recommendations found! Try checking your internet or API key.")
