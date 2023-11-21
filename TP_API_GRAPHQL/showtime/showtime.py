import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    # On définit les méthodes du service qui sont dans le showtime.proto

    def GetListShowtimes(self, request, context):
        schedules = []
        # On parcourt la base de données
        for schedule in self.db:
            # On ajoute le schedule à la liste des schedules
            schedules.append(showtime_pb2.Schedule(date=schedule['date'], movies=schedule['movies']))
        # On renvoie la liste des schedules en utilisant les types (Message) disponibles dans le fichier showtime_pb2.py
        return showtime_pb2.AllSchedule(schedules=schedules)

    def GetShowMoviesByDate(self, request, context):
        for schedule in self.db:
            # Si la date correspond à celle passée en paramètre
            if schedule['date'] == request.date:
                # On renvoie le schedule
                return showtime_pb2.Schedule(date=schedule['date'], movies=schedule['movies'])

    def FindShowtimeByDateAndMovieId(self, request, context):
        for schedule in self.db:
            # Si la date correspond à celle passée en paramètre
            if schedule['date'] == request.date:
                # On parcourt les movies du schedule
                for movie in schedule['movies']:
                    # Si le movie correspond à celui passé en paramètre
                    if movie == request.movieId:
                        # On renvoie un message ShowtimeFound avec found=True
                        return showtime_pb2.ShowtimeFound(found=True)
        # Si on ne trouve pas de showtime, on renvoie un message ShowtimeFound avec found=False
        return showtime_pb2.ShowtimeFound(found=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('localhost:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
