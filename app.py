from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the movie data and similarity matrix
movies = pickle.load(open('/home/choxv/workc/Projects/MovieRecommendationSystem/movie_list.pkl', 'rb'))
similarity = pickle.load(open('/home/choxv/workc/Projects/MovieRecommendationSystem/similarity.pkl', 'rb'))

# Load the original dataset to get poster links
original_data = pd.read_csv('/home/choxv/workc/Projects/MovieRecommendationSystem/imdb_top_1000.csv')

def recommend(movie):
    try:
        index = movies[movies['Series_Title'] == movie].index[0]
    except IndexError:
        return []
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].Series_Title
        # Get poster URL from original data
        poster_url = original_data[original_data['Series_Title'] == movie_title]['Poster_Link'].values[0]
        recommended_movies.append({
            'title': movie_title,
            'poster': poster_url
        })
    
    return recommended_movies

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommendations = recommend(selected_movie)
        # Get poster for selected movie
        selected_poster = original_data[original_data['Series_Title'] == selected_movie]['Poster_Link'].values[0]
        return render_template('index.html', 
                             movie_list=movies['Series_Title'].values,
                             recommendations=recommendations,
                             selected_movie=selected_movie,
                             selected_poster=selected_poster)
    
    return render_template('index.html', 
                         movie_list=movies['Series_Title'].values,
                         recommendations=None,
                         selected_movie=None,
                         selected_poster=None)

if __name__ == '__main__':
    app.run(debug=True)