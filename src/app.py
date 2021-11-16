from dotenv import load_dotenv
from flask import Flask, request, Response

from auth import auth_required
from index_message import get_index_help_message
from product_board import get_aggregated_board_stats, ReturnType, get_product_board_stats

app = Flask(__name__)


@app.route('/', methods=['GET'])
@auth_required
def index():
    message_builder = get_index_help_message()
    return Response(message_builder, mimetype='text/html')


@app.route('/check', methods=['GET'])
@auth_required
def check():
    return {'up': 'ok'}


@app.route('/product/detailed', methods=['GET'])
@auth_required
def advanced():

    include_custom_sizes = request.args.get('include_custom_sizes')
    stats = get_product_board_stats(
        return_type=ReturnType.HTML,
        include_custom_sizes=include_custom_sizes == 'true')
    message_builder = '<h3>current state</h3>'
    message_builder += stats
    return Response(stats, mimetype='text/html')


@app.route('/product/detailed/csv', methods=['GET'])
@auth_required
def advanced_csv():
    include_custom_sizes = request.args.get('include_custom_sizes')
    stats = get_product_board_stats(
        return_type=ReturnType.CSV,
        include_custom_sizes=include_custom_sizes == 'true')
    return Response(stats, mimetype='text/csv')


@app.route('/product/aggregated', methods=['GET'])
@auth_required
def aggregated():
    stats = get_aggregated_board_stats(return_type=ReturnType.HTML)
    message_builder = '<h3>current state</h3>'
    message_builder += stats
    return Response(message_builder, mimetype='text/html')


@app.route('/product/aggregated/csv', methods=['GET'])
@auth_required
def aggregated_csv():
    stats = get_aggregated_board_stats(return_type=ReturnType.CSV)
    return Response(stats, mimetype='text/csv')


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
