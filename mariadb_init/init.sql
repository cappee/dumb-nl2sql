CREATE DATABASE IF NOT EXISTS movies_db;

USE movies_db;


CREATE USER 'py'@'%' IDENTIFIED BY 'esonero';
GRANT ALL PRIVILEGES ON movies_db.* TO 'py'@'%';
FLUSH PRIVILEGES;


-- Directors table
CREATE TABLE directors(
    director_id INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY(director_id)
);

-- Movies table
CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    release_year INT NOT NULL,
    genre VARCHAR(30) NOT NULL,
    director_id INT NOT NULL,
    PRIMARY KEY(movie_id),
    FOREIGN KEY(director_id) REFERENCES directors(director_id)
);

-- Platforms table
CREATE TABLE platforms(
    platform_id INT AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY(platform_id)
);

-- Table that links movies and platform with a many-to-many relationship
CREATE TABLE watch_on(
    movie_id INT NOT NULL,
    platform_id INT NOT NULL,
    PRIMARY KEY(movie_id, platform_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id)
);


INSERT INTO platforms (name) VALUES
('Amazon Prime Video'),
('NOW'),
('Netflix'),
('Paramount+'),
('Disney+');


INSERT INTO directors (name, age) VALUES
('Christopher Nolan', 54),
('Bong Joon-ho', 55),
('David Fincher', 62),
('Ridley Scott', 87),
('Martin Scorsese', 82),
('George Lucas', 80),
('Quentin Tarantino', 62),
('Frank Darabont', 66),
('Robert Zemeckis', 72),
('Francis Ford Coppola', 86),
('Lana Wachowski', 59),
('Hayao Miyazaki', 84),
('Steven Spielberg', 78),
('Peter Jackson', 63),
('Damien Chazelle', 40),
('Todd Phillips', 54),
('George Miller', 80),
('Denis Villeneuve', 57);


INSERT INTO movies (name, release_year, genre, director_id) VALUES
('Inception', 2010, 'Fantascienza', 1),
('Parasite', 2019, 'Dramma', 2),
('Interstellar', 2014, 'Fantascienza', 1),
('The Dark Knight', 2008, 'Azione', 1),
('Fight Club', 1999, 'Dramma', 3),
('Seven', 1995, 'Crime', 3),
('Gladiator', 2000, 'Azione', 4),
('Shutter Island', 2010, 'Thriller', 5),
('Star Wars: A New Hope', 1977, 'Fantascienza', 6),
('Pulp Fiction', 1994, 'Crime', 7),
('The Shawshank Redemption', 1994, 'Dramma', 8),
('Forrest Gump', 1994, 'Dramma', 9),
('The Godfather', 1972, 'Crime', 10),
('The Matrix', 1999, 'Fantascienza', 11),
('Goodfellas', 1990, 'Crime', 5),
('Spirited Away', 2001, 'Animazione', 12),
('Saving Private Ryan', 1998, 'Guerra', 13),
('Back to the Future', 1985, 'Fantascienza', 9),
('The Lord of the Rings: The Fellowship of the Ring', 2001, 'Fantasy', 14),
('The Lord of the Rings: The Return of the King', 2003, 'Fantasy', 14),
('Schindler''s List', 1993, 'Dramma', 13),
('Inglourious Basterds', 2009, 'Guerra', 7),
('Whiplash', 2014, 'Dramma', 15),
('Joker', 2019, 'Dramma', 16),
('Mad Max: Fury Road', 2015, 'Azione', 17),
('Blade Runner 2049', 2017, 'Fantascienza', 18),
('Arrival', 2016, 'Fantascienza', 18),
('Django Unchained', 2012, 'Western', 7),
('The Wolf of Wall Street', 2013, 'Biografico', 5),
('Once Upon a Time in Hollywood', 2019, 'Commedia', 7);


INSERT INTO watch_on (movie_id, platform_id) VALUES
(1, 1), (1, 2),
(2, 3),
(3, 4), (3, 1),
(4, 3),
(6, 3),
(7, 3), (7, 4),
(8, 3), (8, 4),
(9, 5),
(10, 2), (10, 4),
(11, 2),
(12, 3), (12, 4),
(13, 4), (13, 3),
(14, 3), (14, 1),
(15, 3), (15, 2),
(16, 3),
(17, 4), (17, 2),
(18, 3), (18, 1),
(19, 1), (19, 2),
(20, 1), (20, 2),
(21, 1), (21, 2),
(22, 1), (22, 3),
(23, 3),
(24, 3), (24, 1),
(25, 3), (25, 2),
(26, 3),
(27, 3), (27, 4),
(28, 3),
(29, 3), (29, 1),
(30, 3);