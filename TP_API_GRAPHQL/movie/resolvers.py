import json

def resolve_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies['movies']

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'].lower() == _id.lower():
                return movie

def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors

def resolve_movie_with_title(_, info, _title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'].lower() == _title.lower():
                return movie

def resolve_add_movie(_, info, _id, _title, _director, _rating):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        movies['movies'].append({'id': _id, 'title': _title, 'director': _director, 'rating': _rating})
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            json.dump(movies, wfile)
        return {'id': _id, 'title': _title, 'director': _director, 'rating': _rating}

def resolve_delete_movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'].lower() == _id.lower():
                movies['movies'].remove(movie)
                with open('{}/data/movies.json'.format("."), "w") as wfile:
                    json.dump(movies, wfile)
                return "Movie deleted"
        return "Movie not found"