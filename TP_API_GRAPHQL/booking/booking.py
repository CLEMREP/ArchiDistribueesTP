import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('localhost:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
