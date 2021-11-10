import requests
from typing import Dict
import pandas as pd

from config.board_config import RELEVANT_TRELLO_LISTS
from config.trello_config import get_trello_board_call_string


# later, make this a data class
def get_board() -> Dict:
    call = get_trello_board_call_string()
    response = requests.get(call)

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
                if item['name'] in RELEVANT_TRELLO_LISTS}
    return list_ids
