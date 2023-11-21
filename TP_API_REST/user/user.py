from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user),200)
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)

# Récupération des bookings d'un utilisateur
@app.route("/users/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    # Appel du service booking REST
    res = requests.get("http://localhost:3201/bookings/{}".format(userid)).json()
    return make_response(res)

@app.route("/users/infomovies/<userid>", methods=['GET'])
def get_user_movies(userid):
    # Appel du service booking REST
    res = requests.get("http://localhost:3201/bookings/{}".format(userid)).json()
    movies = []
    rvalue = []

    # On boucle sur les dates
    for i in range(len(res['dates'])):
        # On boucle sur les movies
        for movie in res['dates'][i]['movies']:
            # On récupère les movies dans un tableau en appelant le service movie REST
            movies.append(requests.get("http://localhost:3200/movies/{}".format(movie)).json())

    # On boucle sur les movies pour récupérer les infos
    for movie in movies:
        # On récupère les infos du movie dans un tableau en appelant le service movie REST
        rvalue.append(requests.get("http://localhost:3200/movies/{}".format(movie['id'])).json())

    return make_response(jsonify(rvalue),200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
