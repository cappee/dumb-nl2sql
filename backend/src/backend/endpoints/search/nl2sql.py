import re

from backend.endpoints.search.models import Query


class Nl2SQL:

    @staticmethod
    def _movies_by_year(year: str) -> str:
        return f"""
            SELECT m.name, d.name AS director_name, m.release_year, m.genre, GROUP_CONCAT(p.name)
            FROM movies m
            JOIN directors d ON m.director_id = d.director_id
            JOIN watch_on w ON m.movie_id = w.movie_id
            JOIN platforms p ON w.platform_id = p.platform_id
            WHERE release_year = {year}
            GROUP BY m.movie_id;
        """

    @staticmethod
    def _directors_on_netflix() -> str:
        return """
            SELECT DISTINCT d.name, d.age
            FROM directors d
            JOIN movies m ON d.director_id = m.director_id
            JOIN watch_on w ON m.movie_id = w.movie_id
            JOIN platforms p ON w.platform_id = p.platform_id
            WHERE p.name = 'Netflix';
        """

    @staticmethod
    def _scifi_movies() -> str:
        return """
            SELECT m.name, d.name AS director_name, m.release_year, m.genre, GROUP_CONCAT(p.name)
            FROM movies m
            JOIN directors d ON m.director_id = d.director_id
            JOIN watch_on w ON m.movie_id = w.movie_id
            JOIN platforms p ON w.platform_id = p.platform_id
            WHERE genre = 'Fantascienza'
            GROUP BY m.movie_id;
        """

    @staticmethod
    def _movies_by_director_age(age: str) -> str:
        return f"""
            SELECT m.name, d.name AS director_name, m.release_year, m.genre, GROUP_CONCAT(p.name)
            FROM movies m
            JOIN directors d ON m.director_id = d.director_id
            JOIN watch_on w ON m.movie_id = w.movie_id
            JOIN platforms p ON w.platform_id = p.platform_id
            WHERE d.age >= {age}
            GROUP BY m.movie_id;
        """

    @staticmethod
    def _directors_with_multiple_movies() -> str:
        return """
            SELECT d.name, d.age
            FROM directors d
            JOIN movies m ON d.director_id = m.director_id
            GROUP BY d.name
            HAVING COUNT(m.movie_id) > 1;
        """

    def __init__(self, question: str) -> None:
        self._question = question
        self._matched = False

        self._patterns: dict[str, Query] = {
            r"^Elenca i film del (\d{4})\.$": Query(
                sql=self._movies_by_year,
                item_type="film",
                fields=["name", "director_name",  "release_year", "genre", "platforms"]
            ),
            r"^Quali sono i registi presenti su Netflix\?$": Query(
                sql=self._directors_on_netflix,
                item_type="director",
                fields=["name", "age"]
            ),
            r"^Elenca tutti i film di fantascienza\.$": Query(
                sql=self._scifi_movies,
                item_type="film",
                fields=["name", "director_name", "release_year", "genre", "platforms"]
            ),
            r"^Quali film sono stati fatti da un regista di almeno (\d{2}) anni\?$": Query(
                sql=self._movies_by_director_age,
                item_type="film",
                fields=["name", "director_name", "release_year", "genre", "platforms"]
            ),
            r"^Quali registi hanno fatto più di un film\?$": Query(
                sql=self._directors_with_multiple_movies,
                item_type="director",
                fields=["name", "age"]
            )
        }

        # Match the question with the patterns
        # and extract the SQL callable and arguments
        for pattern, query in self._patterns.items():
            match = re.match(pattern, self._question)
            if match:
                self._matched = True
                self._item_type = query["item_type"]
                self._sql_callable = query["sql"]
                self._sql_args = match.groups()
                self._fields = query["fields"]
                break


    def is_valid(self) -> bool:
        """Returns True if the question matches a valid pattern."""
        return self._matched


    def get_sql_query(self) -> str:
        """Returns the SQL query string."""
        if not self._matched:
            raise ValueError("No valid SQL pattern matched.")
        return self._sql_callable(*self._sql_args)

    
    def get_item_type(self) -> str:
        """Returns the item type (e.g., 'film', 'director')."""
        if not self._matched:
            raise ValueError("No valid SQL pattern matched.")
        return self._item_type
    

    def get_fields(self) -> list[str]:
        """Returns the fields to be extracted from the SQL query result."""
        if not self._matched:
            raise ValueError("No valid SQL pattern matched.")
        return self._fields
