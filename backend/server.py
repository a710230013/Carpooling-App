from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/test_get', methods=['GET'])
def get():
    response = {
        'message': 'post test',
        'data': 'hello',
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='192.168.2.39', port=5000, debug=True)
