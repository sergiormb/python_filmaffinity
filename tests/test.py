import csv
import importlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

import python_filmaffinity
import python_filmaffinity.__meta__ as meta_test
from python_filmaffinity import cli
from python_filmaffinity.config import FIELDS_PAGE_DETAIL, FIELDS_PAGE_MOVIES
from python_filmaffinity.exceptions import (
    FilmAffinityConnectionError,
    FilmAffinityInvalidBackend,
    FilmAffinityInvalidLanguage,
)


FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


def response(html):
    return SimpleNamespace(content=html.encode("utf-8"))


def assert_movie_list_shape(movies, exact_fixture=True):
    assert movies
    movie = movies[0]
    for field in FIELDS_PAGE_MOVIES:
        assert movie[field] is not None, field
    if exact_fixture:
        assert movie["id"] == "867354"
        assert movie["title"] == "El caballero oscuro"
        assert movie["rating"] == 8.1
        assert movie["directors"] == ["Christopher Nolan"]
        assert movie["poster"] == "https://pics.filmaffinity.com/a-large.jpg"


def test_search_parses_current_movie_cards(monkeypatch):
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(
        service, "_load_url", lambda *args, **kwargs: response(fixture("search.html"))
    )

    assert_movie_list_shape(service.search(title="Batman"))


def test_search_can_return_pydantic_models(monkeypatch):
    pytest.importorskip("pydantic")
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(
        service, "_load_url", lambda *args, **kwargs: response(fixture("search.html"))
    )

    movies = service.search(title="Batman", as_model=True)

    assert movies[0].id == "867354"
    assert movies[0].title == "El caballero oscuro"


def test_as_model_requires_pydantic(monkeypatch):
    models = importlib.import_module("python_filmaffinity.models")
    monkeypatch.setattr(models, "BaseModel", None)

    with pytest.raises(ImportError, match=r"python-filmaffinity\[models\]"):
        models.movie_to_model({"id": "1"})


def test_as_model_fails_before_request_when_pydantic_is_missing(monkeypatch):
    models = importlib.import_module("python_filmaffinity.models")
    monkeypatch.setattr(models, "BaseModel", None)
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(
        service,
        "_load_url",
        lambda *args, **kwargs: pytest.fail("as_model should fail before requests"),
    )

    with pytest.raises(ImportError, match=r"python-filmaffinity\[models\]"):
        service.get_movie(id="197671", as_model=True)


def test_top_filmaffinity_parses_current_cards(monkeypatch):
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(
        service, "_load_url", lambda *args, **kwargs: response(fixture("top.html"))
    )

    assert_movie_list_shape(service.top_filmaffinity())


def test_top_service_and_recommend_parse_current_cards(monkeypatch):
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(
        service, "_load_url", lambda *args, **kwargs: response(fixture("service.html"))
    )
    monkeypatch.setattr(
        service, "_get_movie_by_id", lambda id, trailer=False, images=False: {"id": id}
    )

    assert_movie_list_shape(service.top_netflix())
    assert service.recommend_netflix() == {"id": "867354"}


def test_get_movie_by_id_with_images(monkeypatch):
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")

    def fake_load_url(url, *args, **kwargs):
        if "filmimages.php" in url:
            return response(fixture("images.html"))
        return response(fixture("detail.html"))

    monkeypatch.setattr(service, "_load_url", fake_load_url)
    movie = service.get_movie(id="197671", images=True)

    for field in FIELDS_PAGE_DETAIL:
        assert movie[field] is not None, field
    assert movie["id"] == "197671"
    assert movie["rating"] == 6.2
    assert movie["votes"] == 68397
    assert movie["country"] == "Estados Unidos"
    assert movie["images"]["posters"][0]["image"].endswith("poster-large.jpg")


def test_get_movie_can_return_pydantic_model(monkeypatch):
    pytest.importorskip("pydantic")
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(
        service, "_load_url", lambda *args, **kwargs: response(fixture("detail.html"))
    )

    movie = service.get_movie(id="197671", as_model=True)

    assert movie.id == "197671"
    assert movie.title == "Piratas del Caribe: La venganza de Salazar"


def test_export_helpers(tmp_path):
    data = [{"id": "867354", "title": "El caballero oscuro", "rating": 8.1}]

    assert json.loads(python_filmaffinity.to_json(data))[0]["id"] == "867354"

    csv_path = tmp_path / "movies.csv"
    python_filmaffinity.to_csv(data, csv_path)
    with csv_path.open(encoding="utf-8") as file_handle:
        rows = list(csv.DictReader(file_handle))
    assert rows[0]["title"] == "El caballero oscuro"

    markdown = python_filmaffinity.to_markdown(data)
    assert "| id | rating | title |" in markdown
    assert "El caballero oscuro" in markdown


def test_default_sqlite_cache_uses_user_cache(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    service = python_filmaffinity.FilmAffinity(cache_backend="sqlite")

    assert service.cache_path.startswith(str(tmp_path))
    assert "python-filmaffinity" in service.cache_path
    assert "python_filmaffinity/cache-film-affinity" not in service.cache_path


class FakeFilmAffinity:
    def __init__(self, lang="es", cache_backend="sqlite"):
        self.lang = lang
        self.cache_backend = cache_backend

    def search(self, title, top=10):
        return [{"id": "867354", "title": title, "year": "2008", "rating": 8.1}]

    def get_movie(self, id, images=False, trailer=False):
        return [{"id": id, "title": "Movie", "year": "2017", "rating": 6.2}][0]

    def top_filmaffinity(self, top=10):
        return [{"id": "809297", "title": "El padrino", "year": "1972", "rating": 9.0}]


def test_cli_search_json(monkeypatch, capsys):
    monkeypatch.setattr(cli, "FilmAffinity", FakeFilmAffinity)

    assert cli.main(["search", "Batman", "--top", "1", "--json"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output[0]["title"] == "Batman"


def test_cli_movie_table(monkeypatch, capsys):
    monkeypatch.setattr(cli, "FilmAffinity", FakeFilmAffinity)

    assert cli.main(["movie", "197671"]) == 0

    output = capsys.readouterr().out
    assert "TITLE" in output
    assert "Movie" in output


def test_cli_top(monkeypatch, capsys):
    monkeypatch.setattr(cli, "FilmAffinity", FakeFilmAffinity)

    assert cli.main(["top", "--kind", "filmaffinity", "--top", "1"]) == 0

    assert "El padrino" in capsys.readouterr().out


def test_invalid_language():
    with pytest.raises(FilmAffinityInvalidLanguage):
        python_filmaffinity.FilmAffinity(lang="abc")


def test_invalid_backend():
    with pytest.raises(FilmAffinityInvalidBackend):
        python_filmaffinity.FilmAffinity(cache_backend="mysqlite")


def test_invalid_connection():
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    with pytest.raises(FilmAffinityConnectionError):
        service._load_url(
            "http://notworking.tz",
            headers={"User-Agent": "Mozilla/5.0"},
            verify=True,
            timeout=1,
            force_server_response=True,
        )


def test_meta_variables():
    for variable, value in meta_test.__dict__.items():
        if variable in ["__builtins__", "__package__", "__doc__"]:
            continue
        assert value is not None, variable


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="set RUN_INTEGRATION=1 to hit filmaffinity.com",
)
def test_live_search_batman():
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    assert_movie_list_shape(service.search(title="Batman", top=1), exact_fixture=False)


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="set RUN_INTEGRATION=1 to hit filmaffinity.com",
)
def test_live_get_movie_images():
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    movie = service.get_movie(id="197671", images=True)
    assert movie["id"] == "197671"
    assert movie["title"]
    assert movie["images"]["posters"]
