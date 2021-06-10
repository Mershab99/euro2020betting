from src.common.constants import *


def find_group(team):
    for group, value in betting_map.items():
        if team in value['teams']:
            return group
    return None
