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
    """Main view when enters the web app.

    Display the welcome message and prompt the user to enter the information of a song

    Returns: rendered html template

    """
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_rec():
    """View to output the recommendations

    Display the recommendations for the song which the user entered

    Returns: rendered html template

    """
    if request.method == 'POST':
        songTitle = request.form['Song Title']
        artist = request.form['Artist']

        try:
            query = "SELECT * FROM songs WHERE songTitle = '{}' AND artist = '{}' LIMIT 1".format(songTitle, artist)
            recommendation = song_manager.session.execute(query).first()

            if recommendation is None:
                logger.warning("Unable to find the corresponding song.")
                return render_template('not_found.html')

            recommendation_dict = dict(recommendation)

            # modify the dictionaries
            recommendation_dict.pop('id')

            user_input = {}
            user_input['Song'] = recommendation_dict.pop('songTitle')
            user_input['Artist'] = recommendation_dict.pop('artist')

            for i in range(1, 11):
                oldKey = "rec" + str(i)
                newKey = "Recommendation " + str(i)
                recommendation_dict[newKey] = recommendation_dict.pop(oldKey)

            return render_template('result.html', user_input=user_input, recommendations=recommendation_dict)
        except:
            traceback.print_exc()
            logger.warning("Not able to display songs, error page returned")
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
