"""
You must create test data that is sufficiently large 
enough to simulate the system (e.g. at minimum
20 motorists, 100 roadside assistance professionals 
and 20 service requests and transactions). You
should write a script to randomly generate these data
"""
import requests
import random

base_url = "http://localhost:8000"

body = {
    "username": "",
    "password":"test12345",
    "password2":"test12345",
    "email":"",
    "first_name":"",
    "last_name":"Smith",
    "user_type":"",
    }

with open("firstnames.txt", "r") as names_file:
    names = names_file.readlines()

customers = []
mechanics = []

AMOUNT_OF_CUSTOMERS = 20
AMOUNT_OF_PROFESSIONALS  = 100
AMOUNT_OF_CALLOUTS = 20

# create 20 motorists (customers as defined in our system)
body["user_type"] = "customer"

for i in range(0, AMOUNT_OF_CUSTOMERS):
    choice = random.randint(0, len(names)-1)

    first_name = f"{names[choice].strip()}"
    username  = f"{first_name}{i}"
    email = f"{username}@gmail.com"

    body["username"] = username
    body["email"] = email
    body["first_name"] = first_name

    response = requests.post(f"{base_url}/register/", data = body)
    if response.status_code == 200:
        customers.append(response.json())
    print(response.json())

# create 100 roadside assistance professionals (mechanics as defined in our system)
body["user_type"] = "mechanic"

for i in range(0, AMOUNT_OF_PROFESSIONALS):
    choice = random.randint(0, len(names)-1)

    first_name = f"{names[choice].strip()}"
    username  = f"{first_name}_pro_{i}"
    email = f"{username}@gmail.com"

    body["username"] = username
    body["email"] = email
    body["first_name"] = first_name

    response = requests.post(f"{base_url}/register/", data = body)
    if response.status_code == 200:
        mechanics.append(response.json())
    print(response.json())

body = {}
body["username"] = customers[0]["username"]
body["password"] = "test12345"

# make login request 
response = requests.post(f"{base_url}/login/", data=body)
token = response.json()['token']

# create 20 callouts
body = {
    "username": "",
    "status": "REVIEWED",
    "location": "address",
    "mechanic": "",
    "rating":"",
    "review":"Great service",
    "description": "Car is broken"
}

headers = {
    "Authorization": f"Token {token}"
}

for i in range(0, AMOUNT_OF_CALLOUTS):
    choice = random.randint(0, len(customers)-1)
    username = customers[choice]["username"]

    choice = random.randint(0, len(mechanics)-1)
    mechanic = mechanics[choice]["username"]

    rating = random.randint(0, 9)

    body["username"] = username
    body["mechanic"] = mechanic
    body["rating"] = rating
    body["location"] = f"{i} Smith Street"

    response = requests.post(f"{base_url}/create_callout/", data=body, headers=headers)

    print(response.json())