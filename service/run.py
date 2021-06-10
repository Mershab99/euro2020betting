import logging
import os
from datetime import datetime as dt

from flask import Flask, request, render_template, redirect
from flask_cors import CORS
from flask_restful import Api

ADMIN_USER = os.environ['ADMIN_USERNAME']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.info("Enabling CORS...")
CORS(app)
if 'LOG_FOLDER' in os.environ:
    app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "file")
    app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")

    # File Logging Setup
    app.config['LOG_DIR'] = os.environ.get("LOG_FOLDER", "/")
    app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "default.log")
    app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "default_www.log")
    app.config['LOG_MAX_BYTES'] = os.environ.get("LOG_MAX_BYTES", 500_000_000)  # 100MB in bytes
    app.config['LOG_COPIES'] = os.environ.get("LOG_COPIES", 5)

    from src.common.flask_logs import LogSetup

    logs = LogSetup()
    logs.init_app(app)


    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response

from src.common.html_helpers import populate_team_table, populate_user_table, populate_top_scorer_table


@app.route('/')
def home():
    return render_template('index.html', team_table=populate_team_table(), user_table=populate_user_table(),
                           player_table=populate_top_scorer_table())


@app.route('/admin/', methods=['POST'])
def admin():
    username = request.form['username']
    password = request.form['password']
    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        return render_template('admin.html')
    else:
        return redirect('/')


@app.route('/admin-post/', methods=['POST'])
def admin_post():
    if 'create_user' in request.form:
        return render_template('create_user.html')
    elif 'report_scores' in request.form:
        return render_template('report_scores.html')

api = Api(app)

# MONGO DRIVER CODE
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://' + os.environ['MONGO_USERNAME'] + ':' + os.environ['MONGO_PASSWORD'] + '@'
            + os.environ['MONGO_HOST'] + ':' + os.environ['MONGO_PORT'] + '/' + os.environ[
                'MONGO_DB'] + '?authSource=admin',
    'db': 'social'
}

from src.resources import status, user

# Resources
api.add_resource(status.Status, '/status')
api.add_resource(user.CreateUser, '/create-user')
api.add_resource(user.Login, '/admin/login')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
