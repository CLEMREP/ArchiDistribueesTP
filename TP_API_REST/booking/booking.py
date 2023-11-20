from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_byid(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
    return make_response(jsonify({"error":"Booking with this UserID not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def create_booking(userid):
    req = request.get_json()

    if 'date' not in req or 'movieid' not in req:
        return make_response(jsonify({"error": "missing arguments (date, movieid)"}), 400)

    date = req['date']
    movieid = req['movieid']
    seancesByDate = requests.get("http://localhost:3202/showmovies/{}".format(date)).json()

    if movieid not in seancesByDate[0]['movies']:
        return make_response(jsonify({"error": "movie not found"}), 400)

    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            date_found = False
            for bookingDate in booking['dates']:
                if bookingDate['date'] == date:
                    date_found = True
                    if movieid not in bookingDate['movies']:
                        bookingDate['movies'].append(movieid)
                        with open('{}/databases/bookings.json'.format("."), "w") as jsf:
                            json.dump({"bookings": bookings}, jsf, indent=2)
                        return make_response(jsonify({"message": "booking added"}), 200)
                    else:
                        return make_response(jsonify({"error": "booking already exists"}), 409)
            if not date_found:
                booking['dates'].append({"date": date, "movies": [movieid]})
                with open('{}/databases/bookings.json'.format("."), "w") as jsf:
                    json.dump({"bookings": bookings}, jsf, indent=2)
                return make_response(jsonify({"message": "booking added"}), 200)
        else:
            bookings.append({"userid": userid, "dates": [{"date": date, "movies": [movieid]}]})
            with open('{}/databases/bookings.json'.format("."), "w") as jsf:
                json.dump({"bookings": bookings}, jsf, indent=2)
            return make_response(jsonify({"message": "booking added"}), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
