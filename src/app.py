from dotenv import load_dotenv
from flask import Flask, request, Response

from product_board import get_aggregated_board_stats, ReturnType, get_product_board_stats

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Welcome to Trello Stats</h1>"


@app.route('/check', methods=['GET'])
def check():
    return {'test': 'ok'}


@app.route('/product/advanced', methods=['GET'])
def advanced():
    include_nas = request.args.get('include_nas')
    stats = get_product_board_stats(
        return_type=ReturnType.JSON,
        include_nas=include_nas == 'true')
    return stats


@app.route('/product/aggregated/csv', methods=['GET'])
def aggregated():
    stats = get_aggregated_board_stats(return_type=ReturnType.CSV)
    return Response(stats, mimetype='text/csv')


@app.route('/product/aggregated', methods=['GET'])
def aggregated_html():
    stats = get_aggregated_board_stats(return_type=ReturnType.HTML)
    return Response(stats, mimetype='text/html')


if __name__ == '__main__':
    load_dotenv()
    # app.run(host='0.0.0.0', port=10444)
    app.run(threaded=True, port=5000)
