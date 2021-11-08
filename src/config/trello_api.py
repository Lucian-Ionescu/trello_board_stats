import requests
from typing import Dict
import pandas as pd

from config.board_config import relevant_lists
from config.trello_config import CALL


# later, make this a data class
def get_board() -> Dict:
    response = requests.get(CALL)

    if response.reason == 'OK':
        return response.json()
    else:
        return {}


def get_cards(board_json: Dict) -> pd.DataFrame:
    cards = board_json['cards']
    return pd.DataFrame.from_dict(cards)


def get_storypoints_custom_field_id(board_json: Dict):
    custom_fields = board_json['customFields']
    storypoints_custom_field_id = [c['id']
                                   for c in custom_fields
                                   if c['name'] == 'Storypoints']
    return storypoints_custom_field_id[0]


def get_list_ids(board_json: Dict):
    list_ids = {item['id']: item['name']
                for item in board_json['lists']
                if item['name'] in relevant_lists}
    return list_ids
