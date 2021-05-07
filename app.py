import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for

from src.add_songs import Songs, SongManager

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
song_manager = SongManager(app)

@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Song database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        songs = song_manager.session.query(Songs).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html', songs=songs)
    except:
        traceback.print_exc()
        logger.warning("Not able to display songs, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """

    try:
        song_manager.add_song(artist=request.form['artist'], title=request.form['title'],
                              year=request.form['year'], acousticness=request.form['acousticness'],
                              danceability=request.form['danceability'], duration_ms=request.form['duraion_ms'],
                              energy=request.form['energy'], instrumental=request.form['instrumental'],
                              liveness=request.form['liveness'], loudness=request.form['loudness'],
                              key=request.form['key'], mode=request.form['mode'], popularity=request.form['popularity'],
                              speechiness=request.form['speechiness'], tempo=request.form['tempo'],
                              valence=request.form['valence'])
        logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display songs, error page returned")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
