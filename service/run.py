import logging
import os

from flask import Flask, request, render_template, redirect, session
from flask_cors import CORS

ADMIN_USER = os.environ['ADMIN_USERNAME']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.info("Enabling CORS...")
CORS(app)
app.secret_key = 'secret'

from src.common.html_helpers import populate_team_table, populate_user_table, populate_top_scorer_table, \
    populate_player_list, populate_team_list


@app.route('/')
def home():
    return render_template('index.html', team_table=populate_team_table(), user_table=populate_user_table(),
                           player_table=populate_top_scorer_table())


@app.route('/admin/', methods=['POST'])
def admin():
    username = request.form['username']
    password = request.form['password']
    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        session['username'] = username
        session['password'] = password
        return render_template('admin.html')
    else:
        return redirect('/')


@app.route('/admin-post/', methods=['POST'])
def admin_post():
    if 'create_user' in request.form:
        return render_template('create_user.html', players=populate_player_list(), teams=populate_team_list(),
                               user_table=populate_user_table())
    elif 'report_scores' in request.form:
        return render_template('report_scores.html', players=populate_player_list(), teams=populate_team_list())


from src.core.managers.mgr_user import create_user
from src.core.managers.mgr_scores import increment_team_win, increment_team_draw, increment_player_goals


@app.route('/create-user-post/', methods=['POST'])
def create_user_post():
    data = request.form
    try:
        create_user(first_name=data['first_name'], last_name=data['last_name'],
                    teams=[data['team1'], data['team2'], data['team3']],
                    player=data['player'])
        return redirect('/')
    except Exception:
        return {
            'message': 'its broke dawg'
        }


@app.route('/report/', methods=['POST'])
def report_player_score():
    data = request.form
    if 'player_scored' in data and data['player_scored'] is not None:
        increment_player_goals(data['player'])
        return {
            'message': 'success'
        }
    elif 'win' in data.keys() and data['win'] is not None:
        val = increment_team_win(team=data['team'])
        return {
            'message': 'success'
        }
    elif 'draw' in data.keys() and data['draw'] is not None:
        increment_team_draw(team=data['team'])
        return {
            'message': 'success'
        }

    return {
        'message': 'failure'
    }


# MONGO DRIVER CODE
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://' + os.environ['MONGO_USERNAME'] + ':' + os.environ['MONGO_PASSWORD'] + '@'
            + os.environ['MONGO_HOST'] + ':' + os.environ['MONGO_PORT'] + '/' + os.environ[
                'MONGO_DB'] + '?authSource=admin',
    'db': 'social'
}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
