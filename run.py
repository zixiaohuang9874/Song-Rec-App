import argparse
import logging.config
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('spotify-rs-pipeline')

import yaml
import joblib
import pandas as pd

from src.add_songs import SongManager, create_db
from src.s3 import upload_file_to_s3, download_file_from_s3
import src.preprocess as preprocess
import src.model as model
import src.recommendation as recommendation
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':

    # Add parsers for running the pipeline (interacting with s3, creating database, uploading data to database, etc.)
    parser = argparse.ArgumentParser(description="Running the pipeline")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for interacting with s3
    sb_s3 = subparsers.add_parser("s3", description="Interact with S3")
    sb_s3.add_argument("--download", default=False, action='store_true', help="If used, will downlaod from S3. ")
    sb_s3.add_argument('--upload', default=False, action='store_true', help="If used, will upload to S3. ")
    sb_s3.add_argument('--s3path', default='s3://2021-msia423-huang-zixiao/raw/data.csv',
                       help="Where to download the data from s3")
    sb_s3.add_argument('--local_path', default='data/sample/data.csv', help="Where to upload data to in S3")

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--songTitle", default="Someone Like You", help="Title of song to be added")
    sb_ingest.add_argument("--artist", default="Adele", help="Artist of song to be added")
    sb_ingest.add_argument("--rank", default=1, help="Rank of the recommended song")
    sb_ingest.add_argument("--recommendedSong", default="The Christmas Waltz", help="Name of the recommended song")
    sb_ingest.add_argument("--recommendedSongArtist", default="Doris Day", help="Artist of the recommended song")
    sb_ingest.add_argument("--duration_ms", default=168333, help="duration of song to be added")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/songs.db',
                           help="SQLAlchemy connection URI for database")

    # Model Pipeline
    # Sub-parser for preprocess the data
    sb_preprocess = subparsers.add_parser('preprocess', description='Preprocess the raw data')
    sb_preprocess.add_argument('--input', '-i', default='data/sample/data.csv', help='Path to input data')
    sb_preprocess.add_argument('--output', '-o', default='data/clean/clean.csv', help='Path to output data')
    sb_preprocess.add_argument('--config', default='config/pipeline.yaml', help='Path to configuration file')

    # Sub-parser for develop the model
    sb_preprocess = subparsers.add_parser('model', description='Develop the model')
    sb_preprocess.add_argument('--input', '-i', default='data/clean/clean.csv', help='Path to input data')
    sb_preprocess.add_argument('--output', '-o', default='models/KMeansModel.joblib', help='Path to output model')
    sb_preprocess.add_argument('--config', default='config/pipeline.yaml', help='Path to configuration file')

    # Sub-parser for generate the recommendations
    sb_preprocess = subparsers.add_parser('rec', description='Generate the recommendations')
    sb_preprocess.add_argument('--input', '-i', default='data/clean/clean.csv', help='Path to input data')
    sb_preprocess.add_argument('--model', '-m', default='models/KMeansModel.joblib', help='Path to the model')
    sb_preprocess.add_argument('--output', '-o', default='data/result/recommendations.csv',
                               help='Path to output recommendations')
    sb_preprocess.add_argument('--config', default='config/pipeline.yaml', help='Path to configuration file')

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 's3':
        if args.download:
            download_file_from_s3(args.local_path, args.s3path)
        elif args.upload:
            upload_file_to_s3(args.local_path, args.s3path)
    elif sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        sm = SongManager(engine_string=args.engine_string)
        sm.add_song(args.songTitle, args.artist, args.rank, args.recommendedSong,
                    args.recommendedSongArtist, args.duration_ms)
        sm.close()
    elif sp_used == 'preprocess':
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        logger.info("Configuration file loaded from %s" % args.config)

        input = pd.read_csv(args.input)
        logger.info('Input data loaded from %s'% args.input)

        output = preprocess.preprocess(input, config['preprocess'])
        output.to_csv(args.output, index=False)
        logger.info("Output saved to %s" % args.output)
    elif sp_used == 'model':
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        logger.info("Configuration file loaded from %s" % args.config)

        input = pd.read_csv(args.input)
        logger.info('Input data loaded from %s' % args.input)

        output = model.model(input, **config['model']['model'])
        joblib.dump(output, args.output)
        logger.info('Output model saved to %s' % args.output)
    elif sp_used == 'rec':
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        logger.info("Configuration file loaded from %s" % args.config)

        input = pd.read_csv(args.input)
        logger.info('Input data loaded from %s' % args.input)

        model = joblib.load(args.model)
        logger.info('Model loaded from %s' % args.model)

        output = recommendation.recommendation(input, model, **config['recommendation']['recommendation'])
        output.to_csv(args.output, index=False)
        logger.info("Recommendations saved to %s" % args.output)
    else:
        parser.print_help()



