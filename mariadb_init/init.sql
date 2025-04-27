CREATE DATABASE IF NOT EXISTS movies_db;

USE movies_db;

-- Create user with only needed privileges
CREATE USER 'py'@'%' IDENTIFIED BY 'esonero';
GRANT ALL PRIVILEGES ON movies_db.* TO 'py'@'%';
FLUSH PRIVILEGES;

-- Directors table
CREATE TABLE directors(
    director_id INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY(director_id),
    UNIQUE(name)
);

-- Movies table
CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    release_year INT NOT NULL,
    genre VARCHAR(30) NOT NULL,
    director_id INT NOT NULL,
    PRIMARY KEY(movie_id),
    FOREIGN KEY(director_id) REFERENCES directors(director_id),
    UNIQUE(name)
);

-- Platforms table
CREATE TABLE platforms(
    platform_id INT AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY(platform_id),
    UNIQUE(name)
);

-- Table that links movies and platform with a many-to-many relationship
CREATE TABLE watch_on(
    movie_id INT NOT NULL,
    platform_id INT NOT NULL,
    PRIMARY KEY(movie_id, platform_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id)
);