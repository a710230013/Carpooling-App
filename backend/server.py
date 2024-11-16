from flask import Flask, request, jsonify
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app)
data = None

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
    global data 
    data = main.calc()
    print(data)
    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# 
data = {
      driver: {
        user_id: "24e5b87f-2809-45eb-98d6-a6312b549527",
        name: "Walter Nguyen",
        gender: "Male",
        driver_rider: "Driver",
        start_location: "45.4215,-75.6972",
        destination_location: "43.7001,-79.4163",
        time_of_travel: "8:49",
        max_detour_distance: "6",
        non_smoking: "FALSE",
        same_gender: "TRUE",
        no_free_seats: "4",
      },
      riders: [
        {
          user_id: "55e6c0f7-aca0-45d2-9bed-7874783b5903",
          name: "Russell Stephens",
          gender: "Male",
          driver_rider: "Rider",
          start_location: "42.9976,-82.3078",
          destination_location: "42.9976,-82.3078",
          time_of_travel: "18:44",
          max_detour_distance: "5",
          non_smoking: "TRUE",
          same_gender: "TRUE",
          no_of_persons: "1",
        },
        {
          user_id: "281bd0c7-a92a-448a-a923-d3f6f5234b31",
          name: "Christopher Petersen",
          gender: "Male",
          driver_rider: "Rider",
          start_location: "42.9849,-81.2453",
          destination_location: "43.7001,-79.4163",
          time_of_travel: "7:04",
          max_detour_distance: "8",
          non_smoking: "FALSE",
          same_gender: "TRUE",
          no_of_persons: "2",
        },
        {
          user_id: "521a5d60-45e1-417a-9558-b273562ee201",
          name: "Teresa Barnes",
          gender: "Female",
          driver_rider: "Rider",
          start_location: "43.7001,-79.4163",
          destination_location: "42.9976,-82.3078",
          time_of_travel: "7:55",
          max_detour_distance: "15",
          non_smoking: "TRUE",
          same_gender: "FALSE",
          no_of_persons: "2",
        },
      ],
    };