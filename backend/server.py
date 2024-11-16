from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/getUser/<id>', methods=['GET'])
def get_user(id):
    user = {
        'id': id,
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    return jsonify(user)
def get():
    response = {
        'message': 'post test',
        'data': 'hello',
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='10.17.32.71', port=5000, debug=True)
