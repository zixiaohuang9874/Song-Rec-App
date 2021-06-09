import logging
import re

import boto3
import botocore

logger = logging.getLogger(__name__)

def parse_s3(s3path):
    """
    Parse the input s3 path to get the bucket name

    Args:
        s3path (str) - s3 path

    Returns:
        s3bucket (str) - s3 bucket name
        s3path (str) - se path
    """
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path, s3path):
    """
    Upload the file in the local path to the given s3 path

    Args:
        local_path (str) - the local path which has the data
        s3path (str) - the s3 path which the data will be uploaded to

    """

    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)

def download_file_from_s3(local_path, s3path):
    """
    Download the file from the given s3 path to local

    Args:
        local_path (str) - local path which the data would be saved to
        s3path (str) - s3 path which has the data

    """

    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.download_file(s3_just_path, local_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data downloaded from %s to %s', s3path, local_path)

