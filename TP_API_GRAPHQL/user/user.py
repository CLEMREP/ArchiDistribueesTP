from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import grpc
import booking_pb2_grpc
import booking_pb2

app = Flask(__name__)

PORT = 3203
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
            res = make_response(jsonify(user),200)
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)

@app.route("/users/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    res = get_booking_by_userid(stub, userid)
    if len(res.bookings) == 0:
        return make_response(jsonify({"error":"Bookings not found for this User ID"}))
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
                movies.append(requests.post("http://localhost:3001/graphql", json={'query': query}).json()['data']['movie_with_id'])
            response.append({"movies":movies})
    return make_response(jsonify(response))



if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

