import logging

logger = logging.getLogger(__name__)

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()


class Songs(Base):
    """Create a data model for the database to be set up for capturing songs

    """

    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    songTitle = Column(String(100), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    rank = Column(Integer, unique=False, nullable=False)
    recommendedSong = Column(String(100), unique=False, nullable=False)
    recommendedSongArtist = Column(String(100), unique=False, nullable=False)
    duration_ms = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Song %r>' % self.songTitle


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

    def add_song(self, songTitle: str, artist: str, rank: int,
                 recommendedSong: str, recommendedSongArtist: str, duration_ms: int) -> None:
        """Seeds an existing database with additional songs.

        Args:
            songTitle: str - Title of song
            artist: str - Artist
            rank: int - Rank of the recommended song
            recommendedSong: str - Title of the recommended song
            recommendedSongArtist: str - Artist of the recommended song
            duration_ms: int - Duration of the song

        Returns:None

        """

        session = self.session
        track = Songs(songTitle=songTitle, artist=artist, rank=rank, recommendedSong=recommendedSong,
                      recommendedSongArtist=recommendedSongArtist, duration_ms=duration_ms)
        session.add(track)
        session.commit()
        logger.info("%s by %s added to database", songTitle, artist)
