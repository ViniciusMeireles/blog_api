# Blog API

Blog API where users can create, read, update and delete (CRUD) posts.
The API is available in English and Portuguese. You can set the language in the request headers.


## Stack used

**Back-end:** [Python](https://www.python.org/), [Django](https://www.djangoproject.com/), 
[Django-Rest-Framework](https://www.django-rest-framework.org/), 
[Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/),
[Cors-Headers](https://pypi.org/project/django-cors-headers/)

**Database:** [PostgreSQL](https://www.postgresql.org/)

**Containerization:** [Docker](https://www.docker.com/)

**Documentation:** [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/), 
[Swagger](https://swagger.io/), [Redoc](https://redoc.ly/)

## Installation

1. Clone the repository by executing the following command:
```bash
git clone https://github.com/ViniciusMeireles/blog_api.git
```
2. Navigate to the project directory:
```bash
cd blog_api
```
3. Start the Docker containers:
```bash
docker compose up --build
```
4. Create a superuser account:
```bash
docker compose run web python manage.py createsuperuser
```

## Running Unit Tests

To run the unit tests for the project using Docker Compose, follow these steps:

1. Make sure Docker and Docker Compose are installed on your system.
2. Navigate to the project directory:
```bash
cd blog_api
```
3. Run the following command to execute the unit tests:
```bash
docker compose run web python manage.py test
```
This command will start a temporary container, set up the test environment, run the unit tests, 
and display the results in the terminal.


## API Documentation 
[![documentation](https://img.shields.io/badge/Documentation-blue)](http://127.0.0.1:8000/api/schema/redoc/)
[![test](https://img.shields.io/badge/Test_API-blue)](http://127.0.0.1:8000/api/schema/swagger-ui/)

- '/api/token/': Obtain a token to authenticate.
- '/api/token/refresh/': Refresh a token.
- '/api/blog/categories/': List all categories or create a new one.
- '/api/blog/categories/{id}/': Retrieve, update or delete a category.
- '/api/blog/posts/': List all posts or create a new one.
- '/api/blog/posts/{id}/': Retrieve, update or delete a post.
- '/api/blog/comments/': List all comments from a post or create a new one.
- '/api/blog/comments/{id}/': Retrieve, update or delete a comment.

To explore the complete API documentation, please visit 
[http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/) or 
[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/). 
This page provides details on endpoints, parameters, and allows you to interactively test various features 
offered by the API.

Make sure you have the server running locally to access the documentation.