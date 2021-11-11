from dotenv import load_dotenv
from flask import Flask, request, Response
from product_board import get_aggregated_board_stats, ReturnType, get_product_board_stats

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "<h1>Welcome to Trello Stats</h1>"


@app.route('/check', methods=['GET'])
def check():
    return {'up': 'ok'}


@app.route('/product/detailed', methods=['GET'])
def advanced():
    include_nas = request.args.get('include_nas')
    stats = get_product_board_stats(
        return_type=ReturnType.HTML,
        include_nas=include_nas == 'true')
    return Response(stats, mimetype='text/html')


@app.route('/product/detailed/csv', methods=['GET'])
def advanced_csv():
    include_nas = request.args.get('include_nas')
    stats = get_product_board_stats(
        return_type=ReturnType.CSV,
        include_nas=include_nas == 'true')
    return Response(stats, mimetype='text/csv')


@app.route('/product/aggregated', methods=['GET'])
def aggregated():
    stats = get_aggregated_board_stats(return_type=ReturnType.HTML)
    return Response(stats, mimetype='text/html')


@app.route('/product/aggregated/csv', methods=['GET'])
def aggregated_csv():
    stats = get_aggregated_board_stats(return_type=ReturnType.CSV)
    return Response(stats, mimetype='text/csv')


if __name__ == '__main__':
    load_dotenv()
    app.run(threaded=True, port=5000)
