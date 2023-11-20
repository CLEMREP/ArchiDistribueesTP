import grpc
from concurrent import futures

from flask import make_response, jsonify

import booking_pb2
import booking_pb2_grpc
import showtime_pb2_grpc
import showtime_pb2
import json


def get_list_showtimes(stub):
    allShowtimes = stub.GetListShowtimes(showtime_pb2.ShowtimeEmpty())
    return allShowtimes.schedules


def find_showtime_by_date_and_movieid(stub, date, movieid):
    showtime = stub.FindShowtimeByDateAndMovieId(showtime_pb2.FindShowtime(date=date, movieId=movieid))
    return showtime


channel = grpc.insecure_channel('localhost:3003')
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
        for booking in self.db:
            if booking['userid'] == request.userid:
                bookings.append(booking_pb2.BookingE(userid=booking['userid'], dates=booking['dates']))
        return booking_pb2.AllBookings(bookings=bookings)

    def GetListBookings(self, request, context):
        bookings = []
        for booking in self.db:
            bookings.append(booking_pb2.BookingE(userid=booking['userid'], dates=booking['dates']))
        return booking_pb2.AllBookings(bookings=bookings)

    def CreateBooking(self, request, context):
        date = request.date
        movieid = request.movieid
        userid = request.userid

        # check if showtime exists
        showtime = find_showtime_by_date_and_movieid(stub, date, movieid) == showtime_pb2.ShowtimeFound(found=True)

        if not showtime:
            return booking_pb2.AllBookings(bookings=[])

        for booking in self.db:
            if booking['userid'] == userid:
                date_found = False
                for bookingDate in booking['dates']:
                    if bookingDate['date'] == date:
                        date_found = True
                        if movieid not in bookingDate['movies']:
                            bookingDate['movies'].append(movieid)
                            return booking_pb2.AllBookings(bookings=self.db)
                        else:
                            return booking_pb2.AllBookings(bookings=[])
                    else:
                        booking['dates'].append({"date": date, "movies": [movieid]})
                        return booking_pb2.AllBookings(bookings=self.db)
                if not date_found:
                    booking['dates'].append({"date": date, "movies": [movieid]})
                    return booking_pb2.AllBookings(bookings=self.db)
            else:
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
