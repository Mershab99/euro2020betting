betting_map = {
    'a': {
        'teams': ['Belgium', 'England', 'France', 'Spain'],
        'win': 7,
        'draw': 2
    },
    'b': {
        'teams': ['Germany', 'Italy', 'Netherlands', 'Portugal'],
        'win': 8,
        'draw': 4
    },
    'c': {
        'teams': ['Croatia', 'Denmark', 'Ukraine'],
        'win': 12,
        'draw': 6
    },
    'd': {
        'teams': ['Poland', 'Sweden', 'Switzerland', 'Russia', 'Turkey'],
        'win': 14,
        'draw': 8
    },
    'e': {
        'teams': ['Austria', 'Czech Republic', 'Scotland', 'Slovakia', 'Wales'],
        'win': 22,
        'draw': 16
    },
    'f': {
        'teams': ['Finland', 'Hungary', 'North Macedonia'],
        'win': 38,
        'draw': 20
    }
}


def team_scoring_map(team):
    for group, value in betting_map.items():
        if team in value['teams']:
            return {
                'win': value['win'],
                'draw': value['draw']
            }
    return None

ADMIN_USERNAME='admin'
ADMIN_PASSWORD='euro2020'