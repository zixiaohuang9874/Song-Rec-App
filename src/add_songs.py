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
    rec1 = Column(String(100), unique=False, nullable=False)
    rec2 = Column(String(100), unique=False, nullable=False)
    rec3 = Column(String(100), unique=False, nullable=False)
    rec4 = Column(String(100), unique=False, nullable=False)
    rec5 = Column(String(100), unique=False, nullable=False)
    rec6 = Column(String(100), unique=False, nullable=False)
    rec7 = Column(String(100), unique=False, nullable=False)
    rec8 = Column(String(100), unique=False, nullable=False)
    rec9 = Column(String(100), unique=False, nullable=False)
    rec10 = Column(String(100), unique=False, nullable=False)



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

    def add_song(self, songTitle: str, artist: str, rec1: str, rec2: str, rec3:str,
                 rec4: str, rec5: str, rec6:str, rec7: str, rec8: str, rec9:str, rec10:str) -> None:
        """Seeds an existing database with additional songs.

        Args:
            songTitle: str - Title of song
            artist: str - Artist
            rec1-rec10: str - Recommended songs

        Returns:None

        """

        session = self.session
        track = Songs(songTitle=songTitle, artist=artist, rec1=rec1, rec2=rec2, rec3=rec3,
                      rec4=rec4, rec5=rec5, rec6=rec6, rec7=rec7, rec8=rec8, rec9=rec9, rec10=rec10)
        session.add(track)
        session.commit()
        logger.info("%s by %s added to database", songTitle, artist)

    def ingest_recommendation(self, df):
        """Ingest a dataframe to the database

        Args:
            df: pandas dataframe - dataframe with recommendations

        """

        session = self.session
        count = 0
        for i in range(len(df)):
            record = {'songTitle': df.iloc[i,0],
                      'artist': df.iloc[i,1],
                      'rec1': df.iloc[i,2],
                      'rec2': df.iloc[i,3],
                      'rec3': df.iloc[i,4],
                      'rec4': df.iloc[i,5],
                      'rec5': df.iloc[i,6],
                      'rec6': df.iloc[i,7],
                      'rec7': df.iloc[i,8],
                      'rec8': df.iloc[i,9],
                      'rec9': df.iloc[i,10],
                      'rec10': df.iloc[i,11]
                      }

            record = Songs(**record)
            session.add(record)
            count += 1

            session.commit()
            logger.debug("Ingested recommendation %d" % i)

        session.commit()
        logger.info("A total of %d recommendations have been added to the database" % count)

        session.close()
