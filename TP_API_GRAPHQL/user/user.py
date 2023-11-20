from flask import Flask, request, jsonify, make_response
import requests
import json
import grpc
import booking_pb2_grpc
import booking_pb2

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

def get_booking_by_userid(stub, userid):
   booking = stub.GetBookingByUserId(booking_pb2.UserId(userid=userid))
   return booking

def get_list_bookings(stub):
   allBookings = stub.GetListBookings(booking_pb2.Empty())
   for booking in allBookings.bookings:
       print(booking)

channel = grpc.insecure_channel('localhost:3002')
stub = booking_pb2_grpc.BookingStub(channel)

get_booking_by_userid(stub, "chris_rivers")
get_list_bookings(stub)

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "User ID not found"}), 400)


@app.route("/users/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    res = get_booking_by_userid(stub, userid)
    if len(res.bookings) == 0:
        return make_response(jsonify({"error": "Bookings not found for this User ID"}))
    response = []
    for booking in res.bookings:
        response.append(booking.userid)
        for date in booking.dates:
            response.append(date.date)
            movies = []
            for movie in date.movies:
                query = """
                query {
                    movie_with_id(_id: """ + '''"''' + str(movie) + '''"''' + """) {id title rating director}
                }
                """
                movies.append(requests.post("http://localhost:3001/graphql", json={'query': query}).json()['data'][
                                  'movie_with_id'])
            response.append({"movies": movies})
    return make_response(jsonify(response))


@app.route("/users/add", methods=['POST'])
def create_user():
    userid = request.form.get("userid")
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User ID already exists"}), 400)

    if 'name' in request.form and 'last_active' in request.form:
        new_user = {
            "id": userid,
            "name": request.form.get('name'),
            "last_active": int(request.form.get('last_active'))
        }

        users.append(new_user)
        # Écriture des données mises à jour dans le fichier
        with open('{}/databases/users.json'.format("."), 'w') as file:
            json.dump({"users": users}, file, indent=2)

        return make_response(jsonify({"success": "User created with success"}), 200)
    else:
        return make_response(jsonify({"error": "Missing parameters (name, last_active)"}), 400)


@app.route("/users/delete/<userid>", methods=['DELETE'])
def delete_user(userid):
    # Recherche de l'utilisateur par ID
    user_to_delete = next((user for user in users if user['id'] == userid), None)

    # Suppression de l'utilisateur si il existe
    if user_to_delete:
        users.remove(user_to_delete)
        # Écriture des données mises à jour dans le fichier
        with open('{}/databases/users.json'.format("."), 'w') as file:
            json.dump({"users": users}, file, indent=2)
        return make_response(jsonify({"success": "Utilisateur supprimé avec succès"}), 200)
    else:
        return make_response(jsonify({"error": "Utilisateur non trouvé"}), 400)


@app.route('/users/update/<userid>', methods=['PUT'])
def update_user(userid):
    # Recherche de l'utilisateur par ID
    user_to_update = next((user for user in users if user['id'] == userid), None)

    # Mise à jour de l'utilisateur si il existe
    if user_to_update:
        if 'name' in request.form:
            user_to_update['name'] = request.form.get('name')
        if 'last_active' in request.form:
            user_to_update['last_active'] = request.form.get('last_active')
        # Écriture des données mises à jour dans le fichier
        with open('{}/databases/users.json'.format("."), 'w') as file:
            json.dump({"users": users}, file, indent=2)
        return make_response(jsonify({"success": "Utilisateur mis à jour avec succès"}), 200)
    else:
        return make_response(jsonify({"error": "Utilisateur non trouvé"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
