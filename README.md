# Django Business and Personnel Manager

Register companies and manage employee information with a CRUD feature.

## Prerequisites

- Python and Django if you want to run the project without Docker
- [Docker Desktop with Docker Compose](https://docs.docker.com/compose/install/)
- Ensure that Docker Desktop is running if you're on Windows or Mac. 
On Linux, ensure that the Docker service is running.

## Run without Docker

To run the project without Docker, you will need to perform database migrations 
and create a superuser account:

1. Run the migrations: 

```bash 
python manage.py makemigrations 
python manage.py migrate
```

2. Create a superuser account and start the Django server:

```bash
python manage.py createsuperuser
python manage.py runserver
```

3. Access the application at http://localhost:8000.

### How to delete data

1. Delete the migrations folder within each Django app directory.


2. If you want to delete users, go to the Django shell:

```bash
python manage.py shell
```

3. Then type:

```bash
from django.contrib.auth.models import User 

User.objects.all().delete()  # To delete all users.

user = User.objects.get(username='choose_the_username')  
user.delete()  # To delete a specific user.

exit()  # To exit the Django shell.
```


## Run with Docker

To run the project with Docker, you will need to build the Docker image, 
start the Docker container, and then perform database migrations and create 
a superuser account within the Docker container.


### Setup

1. Navigate to the root project directory and execute these commands:

```bash
docker-compose build  # Builds the Docker image.
docker-compose up  # Starts the Docker container.
```

2. Access the Docker container's command line:

```bash
docker ps  # Returns the ID of your running container.
docker exec -it <container_id> bash  # Replace <container_id> with the ID from the previous command.
```

3. Inside the Docker container's command line, run the following commands:

```bash
python manage.py makemigrations 
python manage.py migrate
python manage.py createsuperuser
```

The command `python manage.py runserver` is not necessary because
it is used in the `docker-compose.yml` file, under the command key.

4. You can access the Docker container's web server at http://localhost:8000.
8000 refers to the first part of the "8000:8000" string inside the ports key
of 'docker-compose.yml'.

Note. The Docker container has its own isolated environment, 
including its own database. So, if you create a superuser outside Docker, 
this superuser won't exist in the Docker environment.


### Teardown

To stop the container, press Ctrl + c or use the command:

```bash
docker-compose stop
```

The next command will stop the running containers, remove them, and also remove 
the networks and volumes that were created based on the docker-compose.yml configuration.

```bash
docker-compose down
```

If you want to remove the images as well, you can use the --rmi option. 
There are two ways to use it:

```bash
docker-compose down --rmi local  # Removes only the images that were built locally.
docker-compose down --rmi all  # Removes all images used by the docker-compose.yml.
```

Mostly, the docker-compose down --rmi local command removes what
is present in the value of build key from docker-compose.yml file, while
the docker-compose down --rmi all command removes what is under build
as well as image key in your docker-compose.yml. The values of image
key are those images which are pulled from a public Docker registry,
such as Docker Hub, Google Container Registry, Amazon Elastic Container Registry
or Azure Container Registry.


## Run tests

To run tests, type the command:

```bash
python manage.py test
```