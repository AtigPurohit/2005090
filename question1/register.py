import requests

url = 'http://20.244.56.144/train/register'
registration_data = {
    "companyName": "Train Central",
    "ownerName": "Atig",
    "rollNo": "2005090",
    "ownerEmail": "2005090@kiit.ac.in",
    "accessCode": "oJnNPG"
}

response = requests.post(url, json=registration_data)

if response.status_code == 200:
    registration_response = response.json()
    print("Registration successful!")
    print("Company Name:", registration_response["companyName"])
    print("Client ID:", registration_response["clientID"])
    print("Client Secret:", registration_response["clientSecret"])
else:
    print("Registration failed. Status code:", response.status_code)
    print("Response:", response.text)
