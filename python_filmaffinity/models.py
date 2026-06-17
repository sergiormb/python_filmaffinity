"""Optional Pydantic models for FilmAffinity results."""

from typing import Any, Dict, List, Optional


INSTALL_EXTRA = "pip install python-filmaffinity[models]"


try:
    from pydantic import BaseModel, Field
    try:
        from pydantic import ConfigDict
    except ImportError:
        ConfigDict = None
except ImportError:  # pragma: no cover - exercised via import hook tests
    BaseModel = None
    Field = None
    ConfigDict = None


def _require_pydantic():
    if BaseModel is None:
        raise ImportError(
            "Pydantic is required for as_model=True. "
            "Install it with: {}".format(INSTALL_EXTRA)
        )


class _BaseMovieModel(BaseModel if BaseModel is not None else object):
    if ConfigDict is not None:
        model_config = ConfigDict(extra="allow")
    elif BaseModel is not None:
        class Config:
            extra = "allow"


def _list_default():
    return Field(default_factory=list) if Field is not None else []


class Image(_BaseMovieModel):
    image: Optional[str] = None
    thumbnail: Optional[str] = None
    country: Optional[str] = None


class MovieImages(_BaseMovieModel):
    posters: List[Image] = _list_default()
    stills: List[Image] = _list_default()
    promo: List[Image] = _list_default()
    events: List[Image] = _list_default()
    shootings: List[Image] = _list_default()


class Movie(_BaseMovieModel):
    id: Optional[str] = None
    title: Optional[str] = None
    original_title: Optional[str] = None
    year: Optional[str] = None
    duration: Optional[str] = None
    rating: Optional[float] = None
    votes: Optional[Any] = None
    description: Optional[str] = None
    directors: Optional[List[str]] = None
    writers: Optional[List[str]] = None
    music: Optional[List[str]] = None
    cinematography: Optional[List[str]] = None
    actors: Optional[List[str]] = None
    producers: Optional[List[str]] = None
    poster: Optional[str] = None
    country: Optional[str] = None
    genre: Optional[Any] = None
    awards: Optional[List[Dict[str, Any]]] = None
    reviews: Optional[List[Dict[str, Any]]] = None
    images: Optional[MovieImages] = None
    trailer: Optional[List[str]] = None


def movie_to_model(movie):
    """Convert a movie dict to a Pydantic Movie model."""
    _require_pydantic()
    return Movie(**movie)


def movies_to_models(movies):
    """Convert a list of movie dicts to Pydantic Movie models."""
    _require_pydantic()
    return [movie_to_model(movie) for movie in movies]
