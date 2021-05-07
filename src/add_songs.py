import os
import logging.config

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Songs(Base):
    """Create a data model for the database to be set up for capturing songs

    """

    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    year = Column(Integer, unique=False, nullable=False)
    acousticness = Column(Float, unique=False, nullable=False)
    danceability = Column(Float, unique=False, nullable=False)
    duration_ms = Column(Integer, unique=False, nullable=False)
    energy = Column(Float, unique=False, nullable=False)
    instrumental = Column(Float, unique=False, nullable=False)
    liveness = Column(Float, unique=False, nullable=False)
    loudness = Column(Float, unique=False, nullable=False)
    key = Column(Integer, unique=False, nullable=False)
    mode = Column(Integer, unique=False, nullable=False)
    popularity = Column(Integer, unique=False, nullable=False)
    speechiness = Column(Float, unique=False, nullable=False)
    tempo = Column(Float, unique=False, nullable=False)
    valence = Column(Float, unique=False, nullable=False)

    def __repr__(self):
        return '<Track %r>' % self.title


def create_db(engine_string: str) -> None:
    """Create database from provided engine string

    Args:
        engine_string: str - Engine string

    Returns: None

    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")


class SongManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app: Flask - Flask app
            engine_string: str - Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes session

        Returns: None

        """
        self.session.close()

    def add_song(self, title: str, artist: str, year: int, acousticness: float,
                  danceability: float, duration_ms: int, energy: float, instrumental: float,
                  liveness: float, loudness: float, key: int, mode: int, popularity: int,
                  speechiness: float, tempo: float, valence: float) -> None:
        """Seeds an existing database with additional songs.

        Args:
            title: str - Title of song
            artist: str - Artist
            year: int - Year of the song published
            acousticness: float - Acousticness level of the song (Ranges from 0 to 1)
            danceability: float -Danceability level of the song (Ranges from 0 to 1)
            duration_ms: int - Duration of the song
            energy: float - Energy level of the song (Ranges from 0 to 1)
            instrumental: float - Instrumental level of the song (Ranges from 0 to 1)
            Liveness: float - Liveness of the song (Ranges from 0 to 1)
            Loudness: flaot - Loudness level of the song (Float typically ranging from -60 to 0)
            Key: int - Key of the song (Integer from 0 to 11, starting on C as 0, C# as 1 and so on)
            Mode: int - Mode of the song (Minor as 0, Major as 1)
            Popularity: int - Popularity level of the song (Integer ranges from 0 to 100)
            Speechiness: float - Speechiness of the song (Ranges from 0 to 1)
            Tempo: float - Tempo of the song (Float typically ranging from 50 to 150)
            Valence: float - Valence of the song (Ranges from 0 to 1)

        Returns:None

        """

        session = self.session
        track = Songs(artist=artist, title=title, year=year, acousticness=acousticness,
                       danceability=danceability, duration_ms=duration_ms, energy=energy,
                       instrumental=instrumental, liveness=liveness, loudness=loudness,
                       key=key, mode=mode, popularity=popularity, speechiness=speechiness,
                       tempo=tempo, valence=valence)
        session.add(track)
        session.commit()
        logger.info("%s by %s added to database", title, artist)
