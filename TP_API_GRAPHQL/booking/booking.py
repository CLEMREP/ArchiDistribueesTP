import grpc
from concurrent import futures

from flask import make_response, jsonify

import booking_pb2
import booking_pb2_grpc
import showtime_pb2_grpc
import showtime_pb2
import json


# Définition de la fonction pour récupérer les showtimes qui appelle le service gRPC
def get_list_showtimes(stub):
    allShowtimes = stub.GetListShowtimes(showtime_pb2.ShowtimeEmpty())
    return allShowtimes.schedules

# Définition de la fonction pour récupérer un showtime par date et movieid qui appelle le service gRPC
def find_showtime_by_date_and_movieid(stub, date, movieid):
    showtime = stub.FindShowtimeByDateAndMovieId(showtime_pb2.FindShowtime(date=date, movieId=movieid))
    return showtime

# Récupération du service showtime gRPC
channel = grpc.insecure_channel('localhost:3003')
# Et du stub pour avoir les méthodes
stub = showtime_pb2_grpc.ShowtimeStub(channel)

# get_list_showtimes(stub)
print(find_showtime_by_date_and_movieid(stub, "20151130",
                                        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab") == showtime_pb2.ShowtimeFound(
    found=True))


class BookingServicer(booking_pb2_grpc.BookingServicer):
    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookingByUserId(self, request, context):
        bookings = []
        # On parcourt la base de données
        for booking in self.db:
            # Si l'ID de l'utilisateur correspond à celui passé en paramètre
            if booking['userid'] == request.userid:
                # On ajoute le booking à la liste des bookings
                bookings.append(booking_pb2.BookingE(userid=booking['userid'], dates=booking['dates']))
        # On renvoie la liste des bookings en utilisant les types (Message) disponibles dans le fichier booking_pb2.py
        return booking_pb2.AllBookings(bookings=bookings)

    def GetListBookings(self, request, context):
        bookings = []
        # On parcourt la base de données
        for booking in self.db:
            # On ajoute le booking à la liste des bookings
            bookings.append(booking_pb2.BookingE(userid=booking['userid'], dates=booking['dates']))
        # On renvoie la liste des bookings en utilisant les types (Message) disponibles dans le fichier booking_pb2.py
        return booking_pb2.AllBookings(bookings=bookings)

    def CreateBooking(self, request, context):
        date = request.date
        movieid = request.movieid
        userid = request.userid

        # check if showtime exists
        showtime = find_showtime_by_date_and_movieid(stub, date, movieid) == showtime_pb2.ShowtimeFound(found=True)

        if not showtime:
            # return make_response(jsonify({"error": "showtime not found"}), 400)
            # Pas réussi un envoyer autre chose qu'une liste vide donc la gestion des erreurs est pas top. On a pas beaucoup de précision
            # on sait juste que dans User, quand le liste est vide, on renvoie une erreur
            return booking_pb2.AllBookings(bookings=[])

        # Parcours de la base de données
        for booking in self.db:
            # Si l'ID de l'utilisateur correspond à celui passé en paramètre
            if booking['userid'] == userid:
                date_found = False
                # On parcourt les dates
                for bookingDate in booking['dates']:
                    # Si la date correspond à celle passée en paramètre
                    if bookingDate['date'] == date:
                        date_found = True
                        # Si le movieid n'est pas déjà dans la liste des movies
                        if movieid not in bookingDate['movies']:
                            # Alors on l'ajoute
                            bookingDate['movies'].append(movieid)
                            # On retourne la nouvelle liste des bookings
                            return booking_pb2.AllBookings(bookings=self.db)
                        else:
                            # Sinon on renvoie une erreur si le movieid est déjà dans la liste des movies
                            return booking_pb2.AllBookings(bookings=[])
                    else:
                        # Sinon on ajoute la date et le movieid dans la liste des dates
                        booking['dates'].append({"date": date, "movies": [movieid]})
                        return booking_pb2.AllBookings(bookings=self.db)
                # Si la date n'est pas trouvée, on ajoute la date et le movieid dans la liste des dates
                if not date_found:
                    booking['dates'].append({"date": date, "movies": [movieid]})
                    return booking_pb2.AllBookings(bookings=self.db)
            else:
                # Si l'utilisateur n'a aucun booking, on ajoute le booking dans la base de données avec le user et la date
                self.db.append({"userid": userid, "dates": [{"date": date, "movies": [movieid]}]})
                with open('{}/data/bookings.json'.format("."), "w") as jsf:
                    json.dump({"bookings": self.db}, jsf, indent=2)
                return booking_pb2.AllBookings(bookings=self.db)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('localhost:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
