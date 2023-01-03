Fake CSV Generator

Features
* Any user can log in to the system with a username and password.
* Any logged-in user can create any number of data schemas to create datasets with fake data.
* Each such data schema has a name and a list of columns with names and specified data types.
* Users can build the data schema with any number of columns of any type described above.
* Each column also has its own name (which will be a column header in the CSV file).

Technology Stack:
* Python 3.10
* Django
* MDBootstrap
* HTML
* CSS
* AJAX

```shell
Local installation
git clone https://github.com/AriohBelskij/FakeCsv.git
cd fake-csv-generator
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser #create user for tests
python manage.py runserver  # starts Django project
```

![img.png](img.png)
