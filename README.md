# MSiA 423 Spotify Song Recommender System

Project Creator and Developer: Zixiao Huang\
(QA contributions: Lanqi Fei)

## Project Charter
### Vision
Listening to music is an important pastime and a relief from the strenuous work in our everyday life. Yet, with the large amount of songs, people might find it very difficult to find new songs to listen to when they are getting tired of the old songs. This app helps the audience by providing them some top songs based on their previous preferences. With the assistance of this app, people will be able to avoid spending excess amount of time on researching and deciding the song to listen to. 

### Mission
To use the web app, the user will input the title of a song which they enjoyed previously. The user could also specify the number of songs n they want to be recommended. Based on the information which the user entered, the app would then displays the most similar n songs based on clustering algorithms and features such as acousticness and danceability. The data of this project is the [Spotify Dataset 1921-2020, 160k+ Tracks](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks). 

For example, suppose a user is eager to find two songs that are similar to "Bohemian Rhapsody" by the British rock band Queen. The app would then find the two songs which are in the same cluster as "Bohemian Rhapsody" with the smallest distances. Let's say that the top two results returned from the app are "We Will Rock You" by Queen and "Dancing Queen" by the Swedish group ABBA. If the user is not familiar with ABBA before, based on the result of the app, it might prompt him to explore more on this new group and start enjoying it. 

### Success Criteria
#### 1. Machine Learning Metrics
Since the app utilizes a clustering algorithm, it might not make much sense to set a hard threshold to evaluate the overall performance of the recommendation. Instead, we will rely on the reduction in MSE as well as the average silhouette score to determine the numebr of clusters. An optimal silhouette score should probably be larger than 0.5.

#### 2. Business Metrics
For business purpose, an important metric is definitely the number of users who visit the web app. In addition, it might also be a good idea to ask about users' opinions on the recommendations. By evaluating the level of user satisfaction, we could get a better idea of how the web app is performing. A higher level of user satisfaction is likely to generate more profit and revenue, while a lower level indicates the potential flaw in the app and failure.

## Project Overview
<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### 1.1 Acquire the dataset
The original dataset used for this app is from Kaggle. To download the data, please go to [this website](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks)
and click the `Download` button on the top right corner. Note that in order to successfully download the dataset, you would need to use a existing Kaggle account
or create a new Kaggle account to log into the website. The dataset used for this app could also be found in `data/sample/data.csv` in this repository.

#### 1.2 Build a docker image
To use docker in the following data acquisition and database creation steps, you could run the following command to build
the docker image from the root of the repository. 

`docker build -f Dockerfile -t spotify_data .`

#### 1.3 Interact with S3
To begin with, two environment variables, `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` need to be ready and setup in
order to run the following commands. In addition, to upload the file to s3 and download the file from s3, your local data path
and s3 data path could be specified by using `--local_path` and `--s3path` in the commands. If not specified, the default
`local path` is `data/sample/data.csv` and the default `s3_path` is `s3://2021-msia423-huang-zixiao/raw/data.csv`.

##### 1.3.1 Upload data to S3
The following will upload the file, `data/sample/data.csv` to your bucket, assuming that you have environment variables,
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, set in your environment.

`docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY spotify_data s3.py --local_path={Your_local_path} --s3path={Your_s3_path}`

If not using the docker, you can also run the following command:

`python3 src/s3.py --local_path={Your_local_path} --s3_path={Your_s3_path}` 

##### 1.3.2 Download data from S3
The following will download the data file from your bucket, assuming that you have environment variables,
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, set in your environment.

`docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY spotify_data s3.py --local_path={Your_local_path} --s3path={Your_s3_path}`

If not using the docker, you can also run the following command:

`python3 src/s3.py --download --local_path={Your_local_path} --s3_path={Your_s3_path}` 

#### 1.4 Local Database Setup
To create the database in the location configured in `config.py` run: 

`python run.py create_db --engine_string=<engine_string>`

By default, `python run.py create_db` creates a database at `sqlite:///data/songs.db`， if RDS database connection info is not provided.

You can also use docker to create the database in a local SQLite repo. The following command will finish the task:

`docker run spotify_data run.py create_db --engine_string=<engine_string>`

Another way is to set up `SQLALCHEMY_DATABASE_URI` as an environment variable, then run:

`docker run -e SQLALCHEMY_DATABASE_URI spotify_data run.py create_db`

##### 1.4.1 Adding songs 
To add songs to the database:

`python run.py ingest --engine_string=<engine_string> --title=<TITLE> --artist=<ARTIST> --year=<YEAR>
--acousticness=<ACOUSTICNESS> --danceability=<DANCEABILITY> --duration_ms=<DURATION_MS> --energy=<ENERGY>
--instrumental=<INSTRUMENTAL> --liveness=<LIVENESS> --loudness=<LOUDNESS> --key=<KEY> --mode=<MODE>
--popularity=<POPULARITY> --speechiness=<SPEECHINESS> --temp=<TEMPO> --valence=<VALENCE>`

By default, `python run.py ingest` adds *Keep A Song In Your Soul* by Mamie Smith to the SQLite database located in `sqlite:///data/songs.db`.

##### 1.4.2 Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### 1.4.3 Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/songs.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/zixiaohuang/Desktop/Northwestern/MSiA423/Final Project/2021-msia423-Huang-Zixiao/data/songs.db'
```

#### 1.5 Remote Database Setup
Before connecting to the remote database (e.g. database on RDS instance), several things need to be done in advance. First of all, the
`spotify_data` docker image needs to be built. Please refer to the `Build a docker image` session above for more information. In addition,
Northwestern VPN is required in order to connect ot the database. Lastly, five environment variables need to be set up, including `MYSQL_USER`,
`MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT` and `DATABASE_NAME`. Information which is needed to create the database is listed as the following:

```
MYSQL_USER:
MYSQL_PASSWORD:
MYSQL_PORT: 3306
DATABASE_NAME: msia_423_db
MYSQL_HOST: nw-msia423-zixiao.cpfwga9vubbx.us-east-2.rds.amazonaws.com
```

##### 1.5.1 Connecting to Database
The following would connect to the database.

```
docker run -it --rm \
    mysql:5.7.33 \
    mysql \
    -h$MYSQL_HOST \
    -u$MYSQL_USER \
    -p$MYSQL_PASSWORD \
```

After entering the database, to view the table created, use the following commands in this order: `USE msia423_db;`, `DESCRIBE movies;`.
This will display the schema of the created table. 

##### 1.5.2 Creating a database
The following command would create a database/ The default engine_string is specified in `config/flaskconfig.py`.
```
docker run -it \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e DATABASE_NAME \
    spotify_data run.py create_db --engine_string={YOUR_ENGINE_STRING}
```

##### 1.5.3 Adding songs
The following command would add a song to the database.
```
docker run -it \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e DATABASE_NAME \
    spotify_data run.py ingest --engine_string={YOUR_ENGINE_STRING} --title=<TITLE> --artist=<ARTIST> --year=<YEAR>--acousticness=<ACOUSTICNESS> \
    --danceability=<DANCEABILITY> --duration_ms=<DURATION_MS> --energy=<ENERGY> --instrumental=<INSTRUMENTAL> --liveness=<LIVENESS> --loudness=<LOUDNESS> \ 
    --key=<KEY> --mode=<MODE> --popularity=<POPULARITY> --speechiness=<SPEECHINESS> --temp=<TEMPO> --valence=<VALENCE>
```


 
