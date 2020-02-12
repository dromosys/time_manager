# Time Manager

# dev
 * Eclipse (pydev)

# setup local
 1. git clone https://github.com/dromosys/time_manager
 1. pip install -r requirements.txt
 1. cd time_manager
 1. python manage.py makemigrations; python manage.py migrate
 1. python3 manage.py createsuperuser
 1. python3 manage.py collectstatic
 1. python3 manage.py runserver
 1. sqlite3 db/db.sqlite3
 
 # setup docker
```
sudo docker build -t time_manager/time_manager:1.0.0 .
sudo docker run -p 8000:80 -t time_manager/time_manager:1.0.0
```
# login
  * http://localhost:8000/accounts/login/
  * http://localhost:8000/
