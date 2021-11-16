from enum import Enum
from typing import List

import pandas as pd

from config.board_config import STORYPOINTS_ORDERED, STORYPOINTS_NUMERIC, DONE_LISTS, \
    RELEVANT_TRELLO_LISTS
from trello_api import get_board, get_list_ids, get_storypoints_custom_field_id, get_cards

ReturnType = Enum('ReturnType', 'JSON CSV DATAFRAME HTML')


def sort_by_list_and_storypoints(df: pd.DataFrame,
                                 relevant_lists: List[str] = RELEVANT_TRELLO_LISTS,
                                 storypoints_order: List[str] = STORYPOINTS_ORDERED):
    # create temporary categorical attributes for sorting
    df['lists_cat'] = pd.Categorical(df['list'],
                                     categories=relevant_lists,
                                     ordered=True)
    df['storypoints_cat'] = pd.Categorical(df['storypoints'],
                                           categories=storypoints_order,
                                           ordered=True)
    # sort by lists and storypoints
    df.sort_values(['lists_cat', 'storypoints_cat'], inplace=True)
    # return sorted df without categorical attributes
    return df.reset_index(drop=True).drop(columns=['lists_cat', 'storypoints_cat'])


def get_product_board_stats(return_type: ReturnType = ReturnType.JSON, include_custom_sizes: bool = True):
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
    # extract storypoints, use None if field does not exist
    cards_selected['storypoints'] = [a[0] if len(a) > 0 else None for a in aux]

    # drop custom field column
    cards_selected.drop(columns='customFieldItems', inplace=True)
    # count cards per list and storypoints size
    result = cards_selected.groupby(['idList', 'storypoints'], dropna=False).count().reset_index()
    # rename columns
    result.columns = ['list', 'storypoints', 'count']

    if not include_custom_sizes:
        result.dropna(axis=0, inplace=True)

    result = sort_by_list_and_storypoints(result)
    if return_type == ReturnType.CSV:
        return return_df_as_csv(result)
    else:
        if return_type == ReturnType.JSON:
            return return_df_as_json(result)
        else:
            if return_type == ReturnType.HTML:
                return return_df_as_html(result)
    return result


def aggregate_board_stats(df: pd.DataFrame):
    # translate T-Shirt sizes to Fibonacci
    df['storypoints_numeric'] = [STORYPOINTS_NUMERIC.get(s) for s in df.storypoints]
    # compute total storypoints per row
    df['storypoints_numeric_sum'] = df['storypoints_numeric'] * df['count']
    # aggregate by whether list belongs to done (list is implicitly assumed as ongoing otherwise)
    aggregate = df.groupby(df.list.isin(DONE_LISTS)).storypoints_numeric_sum.sum().reset_index()
    # renamings for readability
    aggregate.rename(columns={'list': 'status', 'storypoints_numeric_sum': 'sum'}, inplace=True)
    aggregate.replace({'status': {True: 'done', False: 'in progress'}}, inplace=True)
    # convert to int for readability
    aggregate['sum'] = aggregate['sum'].astype(int)
    return aggregate


def get_aggregated_board_stats(return_type: ReturnType = ReturnType.HTML):
    board_df = get_product_board_stats(return_type=ReturnType.DATAFRAME)
    aggregated_df = aggregate_board_stats(board_df)
    if return_type == ReturnType.CSV:
        return return_df_as_csv(aggregated_df)
    return return_df_as_html(aggregated_df)


def return_df_as_csv(df: pd.DataFrame):
    # convert to csv, na values will be represented as None
    return df.to_csv(na_rep='None', index=False)


def return_df_as_html(df: pd.DataFrame):
    html_builder = '<style>' \
                   'table {text-align: right;}' \
                   'table thead th {text-align: right;}' \
                   '</style>'
    html_builder += df.to_html(header=False, index=False).replace('border="1"', 'border="0.2"')
    return html_builder


def return_df_as_json(df: pd.DataFrame):
    return df.to_json()
