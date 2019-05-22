# email-api
> REST API that allows you to send emails. Created using [Django](https://www.djangoproject.com/) & [Django REST Framework](https://www.django-rest-framework.org/).

## Installation & requirements
The technology stack used in the project:
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](http://www.celeryproject.org/)
- [django-environ](https://github.com/joke2k/django-environ)
- [django-filter](https://github.com/carltongibson/django-filter)

You can easily install the required packages using the `pip` command:
```
pip install -r requirements.txt
```
Then you need to create a `.env` file that will contain the configuration of our django project. The following fields are required: `DEBUG`, `SECRET_KEY`, `DATABASE_URL` and `CELERY_BROKER_URL`. The example: 
```
# Django
DEBUG=False
SECRET_KEY=<secret key>

# Postgres
DATABASE_URL=psql://<username>:<password>@127.0.0.1:8458/database_name

# Celery
CELERY_BROKER_URL=amqp://localhost
```

Now you're ready to start the app:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Usage
### Sending email
To start sending emails, you must first create the `mailbox` and `template` model. Next you make an HTTP POST request:
```sh
curl -X POST -H 'Accept: application/json; indent=4' -u <username>:<password> \
    -d '{"mailbox": "883732a7-a744-4e77-9b8b-0d55eb90d3e6", "template": "fdb6977a-5190-44be-92ae-9288b42146d2", "to": ["user@example.com", "user2@exmaple.com"]}' \
    http://localhost:8000/api/email/
```

### Filtering
The API also allows you to filter sent messages using the `date` and `sent_date` field. To do this, you need to send GET request as below:
```
GET api/email/?date_from=2019-05-22&date_to=2019-05-24              # date filtering
GET api/email/?sent_date_from=2019-05-22&sent_date_to=2019-05-24    # sent_date filtering
```

Created by Mateusz Furga.
