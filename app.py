import streamlit as st
import pickle
import pandas as pd
import requests  # for fetching api details

def fetch_poster(id):
    responses = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1aa3c9eb1386fcd4d7caedf4e313b1b8'.format(id))
    data = responses.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

def recommend(movie):  # movie name is input
  movies_list = similarity[movies[movies['title'] == movie].index[0]]  # similarity values of that matrix with others

  # movie list contains tuples of movies with max similarity
  recommended_movies = []
  recommended_movies_posters = []
  for i in movies_list:
    recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    recommended_movies.append(movies.iloc[i[0]].title)
  return recommended_movies, recommended_movies_posters

# similarity contains sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6] values
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title('FilmPulse: Your favorite movie recommender')

selected_movie_name = st.selectbox(
'Which movie you want to watch?',
movies['title'].values)


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col = st.columns(5)

    for i in range(5):
        with col[i]:
            st.text(names[i])
            st.image(posters[i])
