import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetListShowtimes(self, request, context):
        schedules = []
        for schedule in self.db:
            schedules.append(showtime_pb2.Schedule(date=schedule['date'], movies=schedule['movies']))
        return showtime_pb2.AllSchedule(schedules=schedules)

    def GetShowMoviesByDate(self, request, context):
        for schedule in self.db:
            if schedule['date'] == request.date:
                return showtime_pb2.Schedule(date=schedule['date'], movies=schedule['movies'])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('localhost:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
