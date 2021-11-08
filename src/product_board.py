from config.trello_api import get_board, get_list_ids, get_storypoints_custom_field_id, get_cards


def get_product_board_stats():

    board_json = get_board()

    # get ids of relevant trello lists
    list_ids = get_list_ids(board_json=board_json)

    # get board cards
    cards_df = get_cards(board_json=board_json)

    # get cards only of relevant lists
    cards_selected = cards_df[cards_df.idList.isin(list_ids.keys())]
    # select columns
    cards_selected = cards_selected[['idList', 'customFieldItems', 'shortUrl']]

    # get id of storypoints field
    storypoints_custom_field_id = get_storypoints_custom_field_id(board_json=board_json)

    # convert ids to list names
    cards_selected.replace({'idList': list_ids}, inplace=True)

    # get storypoints per card, this will return a nested list
    aux = [[customField.get('value').get('text').upper()
            for customField in customFields
            if customField['idCustomField'] == storypoints_custom_field_id]
           for customFields in cards_selected.customFieldItems]
    # carve out storypoints, use None if not given
    cards_selected['storypoints'] = [a[0] if len(a) > 0 else None for a in aux]

    # drop custom field column
    cards_selected.drop(columns='customFieldItems', inplace=True)
    # count cards per list and storypoints size
    result = cards_selected.groupby(['idList', 'storypoints'], dropna=False).count().reset_index()
    # rename columns
    result.columns = ['list', 'storypoints', 'count']
    return result.to_json()
    # convert to csv, na values will be represented as None
    return result.to_csv(na_rep='None', index=False)
