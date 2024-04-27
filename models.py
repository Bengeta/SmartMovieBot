import joblib
import pandas as pd

genres_storage = {}
actors_storage = {}
directors_storage = {}

predict_model = None

def prepare_predict_rating_model():
    global predict_model
    predict_model = joblib.load('models/random_forest_model.pkl')

    print('Model loaded')
        
def predict_rating(data):
    global predict_model
    features = [data['metascore'], data['votes'], data['runtime'], data['revenue'], data['main_genre_id'], data['year'], data['main_actor_id'], data['rank'], data['director_id']]
    features_2d = [features]
    return predict_model.predict(features_2d)[0]
        
def encode_actors(actors):
  for actor in actors.split(','):
    actor = actor.strip()
    if actor not in actors_storage:
      actors_storage[actor] = len(actors_storage)
      
def encode_director(director):
  if director not in directors_storage:
    directors_storage[director] = len(directors_storage)
  return directors_storage[director]

def encode_geners(genres):
  for genre in genres.split(','):
    genre = genre.strip()
    if genre not in genres_storage:
      genres_storage[genre] = len(genres_storage)
    
def encode_data():
    filename = 'data/IMDB-Movie-Data.csv'
    data = pd.read_csv(filename)
    
    data['Director'].apply(encode_director)
    data['Actors'].apply(encode_actors)
    data['Genre'].apply(encode_geners)
    
def prepare_models():
    encode_data()
    prepare_predict_rating_model()