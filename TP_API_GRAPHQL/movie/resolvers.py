import json

def resolve_movies(_, info):
    # récupérations des movies
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies['movies']

def movie_with_id(_,info,_id):
    # récupération d'un film avec passage de son ID en paramètre
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        # bouclage sur les différents movies
        for movie in movies['movies']:
            # si l'ID est semblable à celui passé en paramètre, le film en question est retourné
            if movie['id'].lower() == _id.lower():
                return movie

def update_movie_rate(_, info, _id, _rate):
    # modification de la note d'un movie
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        # bouclage sur les différents movies
        for movie in movies['movies']:
            # Si l'ID passé en paramètre correspond, modification du movie en question
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

def resolve_actors_in_movie(movie, info):
    # renvoie les acteurs présents dans un film
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors

def resolve_movie_with_title(_, info, _title):
    # renvoie les informations d'un movie en passant son titre en paramètre
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        # bouclage sur les movies
        for movie in movies['movies']:
            # si le titre du movie correspond à celui passé en paramètre, alors le movie est renvoyé
            if movie['title'].lower() == _title.lower():
                return movie

def resolve_add_movie(_, info, _id, _title, _director, _rating):
    # ajoute un movie en base de données
    with open('{}/data/movies.json'.format("."), "r") as file:
        # chargement de la liste de movies
        movies = json.load(file)
        # ajout d'un movie dans la liste
        movies['movies'].append({'id': _id, 'title': _title, 'director': _director, 'rating': _rating})
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            # remplacement de la liste en base de données pas la nouvelle qui vient d'être modifiéee
            json.dump(movies, wfile)
        return {'id': _id, 'title': _title, 'director': _director, 'rating': _rating}

def resolve_delete_movie_with_id(_, info, _id):
    # suppression d'un movie en fonction de l'id passé en paramètre
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        # bouclage sur la liste de movies
        for movie in movies['movies']:
            # si l'ID est semblable à celui passé en paramètre, le movie sera supprimé de la liste récupérée
            if movie['id'].lower() == _id.lower():
                movies['movies'].remove(movie)
                # Puis la liste modifiée sera renvoyée en base de données pour prendre la place de l'ancienne
                with open('{}/data/movies.json'.format("."), "w") as wfile:
                    json.dump(movies, wfile)
                return "Movie deleted"
        return "Movie not found"