# smc-mess-backend

This is the backend for the SMC Mess application. It is a REST API written in Python using the Django framework. The project is part of the 2023 summer internship at IISER Kolkata.

## Installation

1. Clone the repository

2. Create a virtual environment and activate it

3. Create a `.env` file in the project base directory and add the following

    ```bash
    EMAIL_ID = <youremailid@example.com>
    GOOGLE_APP_PASSWORD = <your-app-password>
    ```

4. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

5. Install celery and redis-server

    ```bash
    sudo apt install celery redis-server
    ```

6. Make migrations

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Create a superuser

    ```bash
    python manage.py createsuperuser
    ```

8. Populate the database with fake data

    ```bash
    python populate_db.py
    ```

9. Run the server

    ```bash
    python manage.py runserver
    ```

10. In a seperate terminal, run the celery worker

    ```bash
    celery -A MessSystemSMC worker -l info
    ```

11. Go to `http://localhost:8000/api` for a summery of all the api endpoints exposed
