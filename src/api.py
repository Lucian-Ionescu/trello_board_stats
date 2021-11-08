from flask import Flask

from product_board import get_product_board_stats

app = Flask(__name__)


@app.route('/check', methods=['GET'])
def check():
    return {'test': 'ok'}


@app.route('/product', methods=['GET'])
def product():
    stats = get_product_board_stats()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10444)
