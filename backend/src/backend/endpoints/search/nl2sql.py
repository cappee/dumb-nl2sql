import re
from typing import Callable

class Nl2SQL:


    @staticmethod
    def movies_by_year(year: str) -> str:
        return f"""
            SELECT *
            FROM movies
            WHERE release_year = {year};
        """


    @staticmethod
    def directors_on_netflix() -> str:
        return """
            SELECT DISTINCT d.name
            FROM directors d
            JOIN movies m ON d.director_id = m.director_id
            JOIN watch_on w ON m.movie_id = w.movie_id
            JOIN platforms p ON w.platform_id = p.platform_id
            WHERE p.name = 'Netflix';
        """


    @staticmethod
    def scifi_movies() -> str:
        return """
            SELECT *
            FROM movies
            WHERE genre = 'Fantascienza';
        """


    @staticmethod
    def movies_by_director_age(age: str) -> str:
        return f"""
            SELECT m.name
            FROM movies m
            JOIN directors d ON m.director_id = d.director_id
            WHERE d.age >= {age};
        """


    @staticmethod
    def directors_with_multiple_movies() -> str:
        return """
            SELECT d.name
            FROM directors d
            JOIN movies m ON d.director_id = m.director_id
            GROUP BY d.name
            HAVING COUNT(m.movie_id) > 1;
        """


    def __init__(self, question: str) -> None:
        self.question = question

        self.patterns: dict[str, tuple[Callable[..., str], str]] = {
            r"^Elenca i film del (\d{4})\.$": (self.movies_by_year, "film"),
            r"^Quali sono i registi presenti su Netflix\?$": (self.directors_on_netflix, "director"),
            r"^Elenca tutti i film di fantascienza\.$": (self.scifi_movies, "film"),
            r"^Quali film sono stati fatti da un regista di almeno (\d{2}) anni\?$": (self.movies_by_director_age, "film"),
            r"^Quali registi hanno fatto più di un film\?$": (self.directors_with_multiple_movies, "director"),
        }


    def get_sql_query(self) -> str:
        for pattern, (query, item_type) in self.patterns.items():
            match = re.match(pattern, self.question)
            if match:
                self.item_type = item_type
                return query(*match.groups())
        return ""
    
    def get_item_type(self) -> str:
        return self.item_type
