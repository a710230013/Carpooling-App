from flask import Flask, request, jsonify
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app)
data = None

@app.route('/getUser/<id>', methods=['GET'])
def get_user(id):
    user = data[id]
    return jsonify(user)

@app.route('/generate', methods=['GET'])
def generate():
    global data 
    data = main.calc()
    print(data)
    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# 