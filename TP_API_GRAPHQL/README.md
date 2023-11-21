# TP MIXTE

## Installation 

- récupérer le projet sur le repo github

Une fois le projet installé vous devez lancer les services dans l'ordre suivant :
- showtime
- booking
- movie 
- user

## Utilisation

### User REST

- CRUD User
- User appelle Booking (gRPC) et Movie (GraphQL)
- get_user_byid : récupère un utilisateur avec son id
- get_user_bookings : récupère les réservations d'un utilisateur
- create_user_booking : crée une réservation pour un utilisateur

### Booking gRPC

- Booking appelle Showtime (gRPC)
- GetBookingByUserId : récupère les réservations d'un utilisateur
- GetListBookings : récupère la liste des réservations
- CreateBooking : crée une réservation

### Movie GraphQL

Un playground est disponible à l'adresse suivante : /graphql

- movie_with_id : récupère un film avec son id
- movie_with_title : récupère un film avec son titre
- update_movie_rate : met à jour la note d'un film
- delete_movie_with_id : supprime un film avec son id
- add_movie : ajoute un film

### Showtime gRPC

- GetListShowtimes : récupère la liste des séances
- GetShowMoviesByDate : récupère la liste des films pour une date donnée
- FindShowtimeByDateAndMovieId : renvoi un bool pour savoir si une séance existe pour une date et un film donné






