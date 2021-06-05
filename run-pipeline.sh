#!/usr/bin/env bash

# Download data from s3 bucket
# python3 run.py s3 --download

# Preprocess the data
python3 run.py preprocess --config=config/pipeline.yaml --input=data/sample/data.csv --output=data/clean/clean.csv

# Build the model
python3 run.py model --config=config/pipeline.yaml --input=data/clean/clean.csv --output=models/KMeansModel.joblib

# Generate recommendations
python3 run.py rec --config=config/pipeline.yaml --input=data/clean/clean.csv --output=data/result/recommendations.csv --model=models/KMeansModel.joblib