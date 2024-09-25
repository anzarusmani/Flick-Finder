import pickle
import streamlit as st
import requests
import random

# Fetch poster for a given movie ID
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommend movies based on a selected movie
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            if poster:
                recommended_movie_posters.append(poster)
                recommended_movie_names.append(movies.iloc[i[0]].title)
        
        # Randomize the recommendations
        combined = list(zip(recommended_movie_names, recommended_movie_posters))
        random.shuffle(combined)
        recommended_movie_names, recommended_movie_posters = zip(*combined) if combined else ([], [])
        
        return list(recommended_movie_names), list(recommended_movie_posters)
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return [], []

# Recommend movies based on genre
def recommend_by_genre(selected_genre):
    genre_movies = others[others['genres'].apply(lambda x: selected_genre in x)]
    recommended_movie_names = genre_movies['title'].values[:5]
    recommended_movie_posters = [fetch_poster(movie_id) for movie_id in genre_movies['movie_id'].values[:5]]
    return recommended_movie_names, recommended_movie_posters

# Recommend movies based on actor
def recommend_by_actor(selected_actor):
    try:
        actor_movies = others[others['cast'].apply(lambda x: selected_actor in x)]
        recommended_movie_names = actor_movies['title'].values
        recommended_movie_posters = [fetch_poster(movie_id) for movie_id in actor_movies['movie_id'].values]
        
        # Randomize the recommendations
        combined = list(zip(recommended_movie_names, recommended_movie_posters))
        random.shuffle(combined)
        recommended_movie_names, recommended_movie_posters = zip(*combined) if combined else ([], [])
        
        return list(recommended_movie_names[:5]), list(recommended_movie_posters[:5])
    except Exception as e:
        st.error(f"Error in actor recommendation: {e}")
        return [], []

# Recommend movies based on director
def recommend_by_director(selected_director):
    try:
        director_movies = others[others['crew'].apply(lambda x: selected_director in x)]
        recommended_movie_names = director_movies['title'].values
        recommended_movie_posters = [fetch_poster(movie_id) for movie_id in director_movies['movie_id'].values]
        
        # Randomize the recommendations
        combined = list(zip(recommended_movie_names, recommended_movie_posters))
        random.shuffle(combined)
        recommended_movie_names, recommended_movie_posters = zip(*combined) if combined else ([], [])
        
        return list(recommended_movie_names[:5]), list(recommended_movie_posters[:5])
    except Exception as e:
        st.error(f"Error in director recommendation: {e}")
        return [], []

# Embed CSS with background image URL
st.markdown(
    """
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=2059&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    .stApp {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        padding: 20px;
        color: white;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    .stSelectbox, .stText {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 5px;
        color: black;
    }
    .stSelectbox label{
    color: black;
    } 
    .stText label {
        color: black;
    }
    .css-1e5wshm {
        color: #FFD700; /* Bright text color */
        background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
        padding: 10px;
        border-radius: 5px;
    }
    .stHeader  {
        font-size: 3em;
        background-color: rgba(0, 0, 0, 0.9); /* More opaque background */
        padding: 20px;
        border-radius: 10px;
        color: #FFD700; /* Bright text color */
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="stHeader">Flick Finder</h1>', unsafe_allow_html=True)
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
others = pickle.load(open('other.pkl', 'rb'))

movie_list = movies['title'].values
genre_list = list(set([genre for sublist in others['genres'] for genre in sublist]))
actor_list = list(set([actor for sublist in others['cast'] for actor in sublist]))
director_list = list(set([director for sublist in others['crew'] for director in sublist]))

col1, col2 = st.columns(2)
with col1:
    selected_movie = st.selectbox("Select a movie from the dropdown", movie_list)
    selected_genre = st.selectbox("Select a genre", genre_list)
with col2:
    selected_actor = st.selectbox("Select an actor", actor_list)
    selected_director = st.selectbox("Select a director", director_list)

if st.button('Show Movie Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(min(5, len(recommended_movie_names)))  # Adjust columns based on the number of recommendations
    for i, col in enumerate(cols):
        if i < len(recommended_movie_names):
            col.text(recommended_movie_names[i])
            col.image(recommended_movie_posters[i])

if st.button('Show Genre Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend_by_genre(selected_genre)
    cols = st.columns(min(5, len(recommended_movie_names)))  # Adjust columns based on the number of recommendations
    for i, col in enumerate(cols):
        if i < len(recommended_movie_names):
            col.text(recommended_movie_names[i])
            col.image(recommended_movie_posters[i])

if st.button('Show Actor Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend_by_actor(selected_actor)
    cols = st.columns(min(5, len(recommended_movie_names)))  # Adjust columns based on the number of recommendations
    for i, col in enumerate(cols):
        if i < len(recommended_movie_names):
            col.text(recommended_movie_names[i])
            col.image(recommended_movie_posters[i])

if st.button('Show Director Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend_by_director(selected_director)
    cols = st.columns(min(5, len(recommended_movie_names)))  # Adjust columns based on the number of recommendations
    for i, col in enumerate(cols):
        if i < len(recommended_movie_names):
            col.text(recommended_movie_names[i])
            col.image(recommended_movie_posters[i])
