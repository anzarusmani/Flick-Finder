import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

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
    .stSelectbox label, .stText label {
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

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
