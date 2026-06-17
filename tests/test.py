import os
from types import SimpleNamespace

import pytest

import python_filmaffinity
import python_filmaffinity.__meta__ as meta_test
from python_filmaffinity.config import FIELDS_PAGE_DETAIL, FIELDS_PAGE_MOVIES
from python_filmaffinity.exceptions import (
    FilmAffinityConnectionError,
    FilmAffinityInvalidBackend,
    FilmAffinityInvalidLanguage,
)


CARD_HTML = """
<div class="fa-card">
  <div class="row movie-card movie-card-1" data-movie-id="867354">
    <div class="mc-poster">
      <img src="/images/empty.gif"
           data-srcset="https://pics.filmaffinity.com/a-msmall.jpg 150w,
                        https://pics.filmaffinity.com/a-large.jpg 400w">
    </div>
    <div class="mc-title">
      <a href="/es/film867354.html">El caballero oscuro</a>
    </div>
    <img class="nflag" alt="Estados Unidos">
    <span class="mc-year">2008</span>
    <div class="avg">8,1</div>
    <div class="count">158.246 <i></i></div>
    <div class="duration">152 min.</div>
    <a class="genre">Accion</a>
    <a class="synop-text">Batman se enfrenta al Joker.</a>
    <div class="mc-director">
      <span class="nb"><a title="Christopher Nolan">Christopher Nolan</a></span>
    </div>
    <div class="mc-cast">
      <span class="nb"><a title="Christian Bale">Christian Bale</a></span>
      <span class="nb"><a title="Heath Ledger">Heath Ledger</a></span>
    </div>
  </div>
</div>
"""

SEARCH_HTML = f"""
<html><body>
  <li class="se-it">{CARD_HTML}</li>
</body></html>
"""

TOP_HTML = f"""
<html><body>
  <ul id="top-movies">
    <li class="content">{CARD_HTML}</li>
  </ul>
</body></html>
"""

SERVICE_HTML = f"""
<html><body>
  <li class="top-movie first">{CARD_HTML}</li>
</body></html>
"""

DETAIL_HTML = """
<html><body>
  <div class="z-movie">
    <div class="rate-movie-box" data-movie-id="197671"></div>
    <span itemprop="name">Piratas del Caribe: La venganza de Salazar</span>
    <dl class="movie-info">
      <dd><span>Titulo original</span>Pirates of the Caribbean</dd>
      <dt>Guion</dt><dd><span class="nb"><a>Jeff Nathanson</a></span></dd>
      <dt>Musica</dt><dd><span class="nb"><a>Geoff Zanelli</a></span></dd>
      <dt>Fotografia</dt><dd><span class="nb"><a>Paul Cameron</a></span></dd>
    </dl>
    <dd itemprop="datePublished">2017</dd>
    <dd itemprop="duration">129 min.</dd>
    <dd itemprop="description">Jack Sparrow vuelve al mar.</dd>
    <div id="movie-rat-avg" content="6,2"></div>
    <span itemprop="ratingCount" content="68.397"></span>
    <span itemprop="director"><span itemprop="name">Joachim Ronning</span></span>
    <li itemprop="actor"><div itemprop="name">Johnny Depp</div></li>
    <img itemprop="image" src="https://pics.filmaffinity.com/poster.jpg">
    <span id="country-img"><img alt="Estados Unidos"></span>
    <span itemprop="genre"><a>Aventuras</a></span>
    <dd class="card-producer"><span class="nb"><a>Jerry Bruckheimer</a></span></dd>
    <dd class="award"><a>2017</a> - Premio de prueba</dd>
    <div class="pro-review">
      <div itemprop="author">Critico</div>
      <div itemprop="reviewBody">Una critica.</div>
      <a href="https://example.com/review">Review</a>
    </div>
  </div>
</body></html>
"""

IMAGES_HTML = """
<html><body>
  <div id="main-image-wrapper"></div>
  <div id="type_imgs_2">
    <div class="colorbox-image">
      <a href="https://pics.filmaffinity.com/poster-large.jpg"
         title="<strong>Pais: </strong>Espana</div>">
        <div style="background-image: url(https://pics.filmaffinity.com/thumb.jpg)"></div>
      </a>
    </div>
  </div>
</body></html>
"""


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
    monkeypatch.setattr(service, "_load_url", lambda *args, **kwargs: response(SEARCH_HTML))

    assert_movie_list_shape(service.search(title="Batman"))


def test_top_filmaffinity_parses_current_cards(monkeypatch):
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(service, "_load_url", lambda *args, **kwargs: response(TOP_HTML))

    assert_movie_list_shape(service.top_filmaffinity())


def test_top_service_and_recommend_parse_current_cards(monkeypatch):
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")
    monkeypatch.setattr(service, "_load_url", lambda *args, **kwargs: response(SERVICE_HTML))
    monkeypatch.setattr(service, "_get_movie_by_id", lambda id, trailer=False, images=False: {"id": id})

    assert_movie_list_shape(service.top_netflix())
    assert service.recommend_netflix() == {"id": "867354"}


def test_get_movie_by_id_with_images(monkeypatch):
    service = python_filmaffinity.FilmAffinity(cache_backend="memory")

    def fake_load_url(url, *args, **kwargs):
        if "filmimages.php" in url:
            return response(IMAGES_HTML)
        return response(DETAIL_HTML)

    monkeypatch.setattr(service, "_load_url", fake_load_url)
    movie = service.get_movie(id="197671", images=True)

    for field in FIELDS_PAGE_DETAIL:
        assert movie[field] is not None, field
    assert movie["id"] == "197671"
    assert movie["rating"] == 6.2
    assert movie["votes"] == 68397
    assert movie["country"] == "Estados Unidos"
    assert movie["images"]["posters"][0]["image"].endswith("poster-large.jpg")


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
