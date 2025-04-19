import re

from backend.endpoints.search.models import Query


class Nl2SQL:

    @staticmethod
    def _movies_by_year(year: str) -> str:
        return f"""
            SELECT m.name, d.name AS director_name, m.release_year, m.genre
            FROM movies m
            JOIN directors d ON m.director_id = d.director_id
            WHERE release_year = {year};
        """

    @staticmethod
    def _directors_on_netflix() -> str:
        return """
            SELECT DISTINCT d.name
            FROM directors d
            JOIN movies m ON d.director_id = m.director_id
            JOIN watch_on w ON m.movie_id = w.movie_id
            JOIN platforms p ON w.platform_id = p.platform_id
            WHERE p.name = 'Netflix';
        """

    @staticmethod
    def _scifi_movies() -> str:
        return """
            SELECT m.name, d.name AS director_name, m.release_year, m.genre
            FROM movies m
            JOIN directors d ON m.director_id = d.director_id
            WHERE genre = 'Fantascienza';
        """

    @staticmethod
    def _movies_by_director_age(age: str) -> str:
        return f"""
            SELECT m.name, d.name AS director_name, m.release_year, m.genre
            FROM movies m
            JOIN directors d ON m.director_id = d.director_id
            WHERE d.age >= {age};
        """

    @staticmethod
    def _directors_with_multiple_movies() -> str:
        return """
            SELECT d.name
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
                fields=["name", "director_name",  "release_year", "genre"]
            ),
            r"^Quali sono i registi presenti su Netflix\?$": Query(
                sql=self._directors_on_netflix,
                item_type="director",
                fields=["name"]
            ),
            r"^Elenca tutti i film di fantascienza\.$": Query(
                sql=self._scifi_movies,
                item_type="film",
                fields=["name", "director_name", "release_year", "genre"]
            ),
            r"^Quali film sono stati fatti da un regista di almeno (\d{2}) anni\?$": Query(
                sql=self._movies_by_director_age,
                item_type="film",
                fields=["name", "director_name", "release_year", "genre"]
            ),
            r"^Quali registi hanno fatto più di un film\?$": Query(
                sql=self._directors_with_multiple_movies,
                item_type="director",
                fields=["name"]
            )
        }

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
        return self._matched


    def get_sql_query(self) -> str:
        if not self._matched:
            raise ValueError("No valid SQL pattern matched.")
        return self._sql_callable(*self._sql_args)

    
    def get_item_type(self) -> str:
        if not self._matched:
            raise ValueError("No valid SQL pattern matched.")
        return self._item_type
    

    def get_fields(self) -> list[str]:
        if not self._matched:
            raise ValueError("No valid SQL pattern matched.")
        return self._fields
