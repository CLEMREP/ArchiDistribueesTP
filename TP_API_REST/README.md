# UE-AD-A1-REST

## Installation

- récupérer le projet sur le repo github

## Utilisation

### User REST

- get_user_byid : récupère un utilisateur avec son id
- get_user_bookings : récupère les réservations d'un utilisateur
- get_user_movies : récupère les films d'un utilisateur

### Booking

- get_json : récupère la liste des réservations
- get_booking_byid : récupère une réservation avec son id
- create_booking : crée une réservation

### Movie

- get_json : récupère la liste des films
- get_movie_byid : récupère un film avec son id
- get_movie_bytitle : récupère un film avec son titre
- create_movie : crée un film
- update_movie_rating : met à jour la note d'un film
- del_movie : supprime un film avec son id

### Showtime

- get_schedule : récupère la liste des séances
- get_movies_bydate : récupère la liste des films (séances) pour une date donnée