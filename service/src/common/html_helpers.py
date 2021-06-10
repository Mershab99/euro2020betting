from flask_table import Table, Col

from src.core.managers.mgr_scores import get_all_team_stats
from src.core.managers.mgr_user import get_all_user_scores


class TeamTable(Table):
    name = Col('name')
    wins = Col('wins')
    draws = Col('draws')

class UserTable(Table):
    first_name = Col('first_name')
    last_name = Col('last_name')
    score = Col('score')


def populate_team_table():
    stats = get_all_team_stats()
    table = TeamTable(stats)
    return table


def populate_user_table():
    stats = get_all_user_scores()
    table = UserTable(stats)
    return table