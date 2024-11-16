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

@app.route('/generate', methods=['GET'])
def generate():
    # call some function to generate the data
    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
