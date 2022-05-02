
## Setup
1) Clone this project: ```git clone https://github.com/SeanOverton/django-csit314.git```
2) Install dependencies: ```pip install -r requirements.txt```
3) Run ```python -c "import secrets; print(secrets.token_urlsafe())"``` to generate a secret key. 
4) Copy the contents of example .env-EXAMPLE and add your secret key generated from the last command into this file. Save this file as **.env** in the root directory. 
  File contents should look like ```DJANGO_SECRET_KEY=<your_secret_key>```
5) ```python manage.py makemigrations```
6) ```python manage.py migrate```
7) Run the server locally: ```python manage.py runserver```

## To access the admin dashbaord on the server:
1) python manage.py createsuperuser
2) This will prompt you for user details. Complete this and remember these details.
3) Navigate to: http://localhost:8000/admin/ to login to the admin dashboard and access DB directly.

## To test server (postman):
1) Import PostmanRequestsCollection.json into Postman app.
2) Send a sign up request.
3) Send a login request.
4) This will return a token that needs to be added to any of the other requests as a header to authenticate with the server. ```Authorization: Token <your_token>```

## NOTE:
- Environment File Required.
[^postmansetup]: Postman requests test setup. Import PostmanRequestsCollection.json into [Postman](https://www.postman.com/downloads/)
