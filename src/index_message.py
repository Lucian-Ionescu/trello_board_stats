def get_index_help_message():
    message_builder = '<h1>Trello Board Stats</h1>'
    message_builder += '<h2>Product (aggregated)</h2>'
    message_builder += '<ul>' \
                       '<li>' \
                       '<a href="/product/aggregated">aggregated in progress vs. done</a>' \
                       '</li>' \
                       '<li>' \
                       '<a href="/product/aggregated/csv">aggregated in progress vs. done (CSV)</a>' \
                       '</li>' \
                       '</ul>'
    message_builder += '<h2>Product (detailed)</h2>'
    message_builder += '<ul>' \
                       '<li>' \
                       '<a href="/product/detailed">detailed per list/storypoints</a>' \
                       '</li>' \
                       '<li>' \
                       '<a href="/product/detailed/csv">detailed per list/storypoints (CSV)</a>' \
                       '</li>' \
                       '<li>' \
                       '<a href="/product/detailed?include_custom_sizes=true">detailed per list/' \
                       'storypoints, including custom storypoint entries</a>' \
                       '</li>' \
                       '<li>' \
                       '<a href="/product/detailed/csv?include_custom_sizes=true">detailed per list/' \
                       'storypoints, including custom storypoint entries (CSV)</a>' \
                       '</li>' \
                       '</ul>'
    return message_builder