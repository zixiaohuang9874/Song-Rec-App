import argparse

import logging.config
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('spotify-rs-pipeline')

from src.add_songs import SongManager, create_db
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--artist", default="Mamie Smith", help="Artist of song to be added")
    sb_ingest.add_argument("--title", default="Keep A Song In Your Soul", help="Title of song to be added")
    sb_ingest.add_argument("--year", default=1920, help="Year of song to be added")
    sb_ingest.add_argument("--acousticness", default=0.991, help="Acousticness of song to be added")
    sb_ingest.add_argument("--danceability", default=0.598, help="danceability of song to be added")
    sb_ingest.add_argument("--duration_ms", default=168333, help="duration of song to be added")
    sb_ingest.add_argument("--energy", default=0.224, help="Energy of song to be added")
    sb_ingest.add_argument("--instrumental", default=0.000522, help="instrumentalness of song to be added")
    sb_ingest.add_argument("--liveness", default=0.379, help="liveness of song to be added")
    sb_ingest.add_argument("--loudness", default=-12.628, help="loudness of song to be added")
    sb_ingest.add_argument("--key", default=5, help="key of song to be added")
    sb_ingest.add_argument("--mode", default=0, help="mode of song to be added")
    sb_ingest.add_argument("--popularity", default=12, help="popularity of song to be added")
    sb_ingest.add_argument("--speechiness", default=0.0936, help="speechiness of song to be added")
    sb_ingest.add_argument("--tempo", default=149.976, help="tempo of song to be added")
    sb_ingest.add_argument("--valence", default=0.634, help="valence of song to be added")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/songs.db',
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        tm = SongManager(engine_string=args.engine_string)
        tm.add_song(args.title, args.artist, args.year, args.acousticness, args.danceability, args.duration_ms,
                    args.energy, args.instrumental, args.liveness, args.loudness, args.key, args.mode, args.popularity,
                    args.speechiness, args.tempo, args.valence)
        tm.close()
    else:
        parser.print_help()



