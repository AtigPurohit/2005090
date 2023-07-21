from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Assuming you have functions to obtain the authorization token and fetch train data
def get_authorization_token():
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
        # Registration successful
        registration_response = response.json()
        print("Registration successful!")
    else:
        print("Registration failed. Status code:", response.status_code)
        print("Response:", response.text)
    token = registration_response["access_token"]
    return token
    pass

def get_real_time_train_data(authorization_token):
        # Implement the logic to fetch details for a specific train using the token
    headers = {
        'Authorization': f'Bearer {authorization_token}'
    }
    response = requests.get('http://20.244.56.144/train/trains', headers=headers)
    
    if response.status_code == 200:
        train_data = response.json()
        return train_data
    else:
        # Handle any errors that might occur during the API request
        print(f"Error: {response.status_code}, {response.text}")
        return None

    pass

def get_train_details(train_id, authorization_token):
    # Obtain the authorization token to access the train data
    authorization_token = get_authorization_token()
    if not authorization_token:
        return "Failed to obtain authorization token.", 401

    # Fetch the real-time train details for the specific train using the authorization token
    train_details = get_train_details(train_id, authorization_token)
    if not train_details:
        return "Failed to fetch train details.", 500

    # You can format and return the train_details JSON data as required
    response = jsonify(train_details)
    return response
    pass

@app.route('/trains/schedule', methods=['GET'])
def get_trains_schedule():
    # Obtain the authorization token to access the train data
    authorization_token = get_authorization_token()
    if not authorization_token:
        return "Failed to obtain authorization token.", 401

    # Fetch the real-time train data using the authorization token
    train_data = get_real_time_train_data(authorization_token)
    if not train_data:
        return "Failed to fetch train data.", 500

    # Calculate the time window of the next 12 hours from the current time
    current_time = datetime.now()
    twelve_hours_from_now = current_time + timedelta(hours=12)

    # Filter trains departing in the next 30 minutes or within the next 12 hours (including delayed departures)
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

    # Sort the trains as per the specified criteria
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
            -departure_time.timestamp()  # Convert to timestamp for descending order of departure time
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
