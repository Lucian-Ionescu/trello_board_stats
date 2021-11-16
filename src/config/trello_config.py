import os


def get_trello_board_call_string():
    _token = os.environ['trello_key']
    _key = os.environ['trello_token']

    return f'https://api.trello.com/1/boards/geUPhL4h?key={_token}&token={_key}&fields=all&actions=all' \
           '&action_fields=all' \
           '&actions_limit=1000&cards=open' \
           '&card_fields=all&card_attachments=false' \
           '&labels=all&lists=all' \
           '&list_fields=all&members=all' \
           '&member_fields=all&checklists=all' \
           '&checklist_fields=all&organization=false' \
           '&customFields=true' \
           '&card_customFieldItems=true'
