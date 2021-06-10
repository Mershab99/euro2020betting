from src.core.managers.mgr_scores import get_all_team_scores
from src.mongo.datastore.datastore import Datastore


class UserDataStore(Datastore):
    def __init__(self):
        super().__init__('users')

    def __update_fields(self, first_name, last_name, fields_to_update):
        return self.collection.update_one({
            'first_name': first_name,
            'last_name': last_name
        }, {'$set': fields_to_update})

    def create_user(self, first_name, last_name, teams, player):
        existing_user = self.collection.find_one({
            'first_name': first_name,
            'last_name': last_name
        })
        if existing_user:
            raise KeyError("a user with that name already exists")

        user = self.collection.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'teams': teams,
            'player': player
        })

        return user is not None

    def get_user(self, first_name, last_name):
        existing_user = self.collection.find_one({
            'first_name': first_name,
            'last_name': last_name
        })
        if existing_user:
            return existing_user
        else:
            raise KeyError('invalid user')

    def get_all_users(self):
        return self.collection.find({})


user_ds = UserDataStore()


def create_user(first_name, last_name, teams, player):
    return user_ds.create_user(first_name, last_name, teams, player)


def get_user_score(first_name, last_name):
    user = user_ds.get_user(first_name, last_name)


def get_all_user_scores():
    all_users = user_ds.get_all_users()
    all_team_scores = get_all_team_scores()
    user_list = []
    for user in all_users:
        user_score = 0
        for team in user['teams']:
            user_score += all_team_scores[team]
            # Player score
            # user_score +=
        user_list.append({
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'score': user_score
        })
    return user_list
