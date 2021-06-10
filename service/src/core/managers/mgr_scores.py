import os

from src.common.constants import betting_map, team_scoring_map
from src.mongo.datastore.datastore import Datastore

ROSTER_URL = os.environ['ROSTER_URL']


class TeamsDataStore(Datastore):
    def __init__(self):
        super().__init__('teams')

    def get_teams(self):
        return self.collection.find_one({})


class PlayerDatastore(Datastore):
    def __init__(self):
        super().__init__('players')

    def get_player(self, player):
        found = self.collection.find_one({
            'name': player
        })
        if found:
            return found
        else:
            return None

    def add_player(self, player):
        if self.get_player(player) is None:
            self.collection.insert_one({
                'name': player,
                'goals': 0
            })

    def add_players(self, players):
        out_docs = [{
            'name': player,
            'goals': 0
        } for player in players]
        return self.collection.insert_many(out_docs)

    def increment_player_goal(self, player):
        current_player = self.get_player(player)

        if current_player:
            current_player['goals'] = current_player['goals'] + 1

            self.collection.update_one({
                'name': player
            }, current_player)

    def get_all_players(self):
        return self.collection.find({}, {'_id': 0})


teams_ds = TeamsDataStore()
player_ds = PlayerDatastore()


def extract_players(data):
    value = data.split(':')[1].split('<')[0]
    return value.split(',')


def populate_mongo_with_players():
    if player_ds.collection.find_one({}) is None:

        import requests

        data = requests.get(ROSTER_URL).text
        all_teams = teams_ds.get_teams()['data']
        for team in all_teams:
            team_title = data.find("{} EURO 2020 squad".format(team['name']))
            gks = data.find("Goalkeepers", team_title)
            defs = data.find("Defenders", team_title)
            mids = data.find("Midfielders", team_title)
            fwds = data.find("Forwards", team_title)
            end = data.find('</p>', fwds)

            gks = extract_players(data[gks:defs])
            defs = extract_players(data[defs:mids])
            mids = extract_players(data[mids:fwds])
            fwds = extract_players(data[fwds:end])

            players = gks + defs + mids + fwds
            player_ds.add_players(players)


populate_mongo_with_players()


def populate_mongo_with_teams():
    team_data = []
    for group, value in betting_map.items():
        for team in value['teams']:
            team_data.append({
                'name': team,
                'wins': 0,
                'draws': 0
            })
    if teams_ds.collection.find_one({}) is None:
        teams_ds.collection.insert_one({
            'data': team_data
        })


def get_all_team_scores():
    team_list = {}
    all_teams = teams_ds.get_teams()
    for team in all_teams['data']:
        point_map = team_scoring_map(team['name'])
        score = (point_map['win'] * team['wins']) + (point_map['draw'] * team['draws'])
        team_list[team['name']] = score
    return team_list


def get_all_team_stats():
    return teams_ds.get_teams()['data']


def get_all_player_stats():
    return [player for player in player_ds.get_all_players()]


populate_mongo_with_teams()
