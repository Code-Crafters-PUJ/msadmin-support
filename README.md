# msadmin-support

To run the microservice, you need to have the .env file created.

To do that:
1. Copy the example.env file and rename it to .env.
2. Then complete the environment variables with your own credentials.

3. To install the dependencies, run the following command, this proyect uses python > 3.10:
```bash
pip install -r requirements.txt
```
4. To create the database, run the following command:
```bash
python manage.py migrate
```
5. To create the mock data, run the following command:
```bash
python manage.py populate_mock_data
```
6. To run the microservice, run the following command:
```bash
python manage.py runserver
```
7. To run the tests, run the following command:
```bash
python manage.py test
```


