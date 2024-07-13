# File Drop App

This is a file uploader app built with Django and Docker. It allows users to upload file to S3.

## Installation

### Prerequisites
- Docker
- Docker Compose

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bmyantis/rns_test_project.git
   cd rns_test_project
2. **rename env-sample as .env and fill all variables based on your data**
    the value of variable ENCRYPTION_KEY should be base64 format
2. **Build the Docker image:**
    docker-compose build
3. **Start the Docker containers:**
    docker-compose up
4. **Run Migrations:**
    - docker exec -it <container_id> bash
    - python manage.py migrate
5. **Create a new user:**
    curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://localhost:8000/api/auth/users/
6. **Obtain authentication token:**
    - curl -X POST -H "Content-Type: application/json" -d '{"username": "your-username", "password": "your-password"}' http://localhost:8000/api/auth/token/login/
    - Copy the authentication token from the response.

### Usage
- With the authentication token obtained, you can manage create and list file using the following endpoints:
    - http://localhost:8000/api/filedrop/
- Use the token in the Authorization header for authentication:
curl -H "Authorization: Token your-auth-token" http://localhost:8000/api/filedrop/

### API Endpoints
- `/api/auth/users/`: User registration endpoint.
- `/api/auth/token/login/`: Obtain authentication token endpoint.
- `/api/filedrop/`: FileDrop management endpoint.

## Run Unit Test
- run `docker exec -it <container id> bash`
- run `coverage run --source='.' manage.py test tests/`
- run `coverage report`