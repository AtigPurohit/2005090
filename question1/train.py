from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_auth_token():
    url = 'http://20.244.56.144/train/auth'
    registration_data = {
    "companyName":"Train Central",
    "clientID":"980e563c-1aa5-4187-bcc8-aad231b3abb5",    
    "ownerName":"Atig",
    "ownerEmail":"2005090@kiit.ac.in",
    "rollNo":"2005090",
    "clientSecret":"JUlvROmQBJTVsrIg"
    }
    
    response = requests.post(url, json=registration_data)

    if response.status_code == 200:
        registration_response = response.json()
        print("registration successfull")
    else:
        print("Registration failed")
    
    token = registration_response["access_token"]
    return token


def get_realtime_traindata(auth_token):
    
    headers = { 'Authorization': f'Bearer {auth_token}'}

    response = requests.get('http://20.244.56.144/train/trains', headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error")

def get_details(train_id, auth_token):
    auth_token = get_auth_token()
    if not auth_token:
        return "Failed to get auth token,"

    train_details = get_details(train_id, auth_token)
    if not train_details:
        return "Failed to get train details"

    response = jsonify(train_details)
    return response

@app.route('/trains/schedule', methods=['GET'])
def get_schedule():
    authorization_token = get_auth_token()
    if not authorization_token:
        return "Failed to obtain authorization token.", 401

    train_data = get_realtime_traindata(authorization_token)
    if not train_data:
        return "Failed to fetch train data.", 500

    current_time = datetime.now()
    twelve_hours_from_now = current_time + timedelta(hours=12)

    def is_valid_departure_time(train):
        departure_time = datetime(
            current_time.year,
            current_time.month,
            current_time.day,
            train['departureTime']['Hours'],
            train['departureTime']['Minutes']
        ) + timedelta(minutes=train['delayedBy'])
        return departure_time > current_time and departure_time <= twelve_hours_from_now

    trains_to_display = [train for train in train_data if 'departureTime' in train and is_valid_departure_time(train)]

    def sorting_key(train):
        departure_time = datetime(
            current_time.year,
            current_time.month,
            current_time.day,
            train['departureTime']['Hours'],
            train['departureTime']['Minutes']
        ) + timedelta(minutes=train['delayedBy'])
        return (
            train['price']['sleeper'],
            -train['seatsAvailable']['sleeper'],
            -departure_time.timestamp() 
        )

    sorted_trains = sorted(trains_to_display, key=sorting_key)

    # Format the response
    trains_schedule = []
    for train in sorted_trains:
        train_schedule = {
            'train_id': train['trainNumber'],
            'train_name': train['trainName'],
            'departure_time': datetime(
                current_time.year,
                current_time.month,
                current_time.day,
                train['departureTime']['Hours'],
                train['departureTime']['Minutes']
            ).strftime("%Y-%m-%d %H:%M:%S"),
            'seats_available_sleeper': train['seatsAvailable']['sleeper'],
            'seats_available_ac': train['seatsAvailable']['AC'],
            'price_sleeper': train['price']['sleeper'],
            'price_ac': train['price']['AC'],
            'delayed_by': train['delayedBy']
        }
        trains_schedule.append(train_schedule)

    response = jsonify(trains_schedule)
    return response


if __name__ == '__main__':
    app.run(debug=True)