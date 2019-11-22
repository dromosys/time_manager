# Time Manager

# dev
 * Eclipse (pydev)

# setup
 1. git clone https://github.com/dromosys/time_manager
 1. pip install -r requirements.txt
 1. cd time_manager
 1. python3 manage.py makemigrations
 1. python3 manage.py migrate
 1. python3 manage.py createsuperuser
 1. python3 manage.py collectstatic
 1. python3 manage.py runserver
 1. sqlite3 db/db.sqlite3
 
# login
  * http://localhost:8000/accounts/login/
  * http://localhost:8000/
  
 # apache config
```
<Directory /home/path/time_manager>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

WSGIDaemonProcess django python-path=/home/path/time_manager python-home=/home/path/venv
WSGIProcessGroup django
WSGIScriptAlias /time /home/path/time_manager/time_manager/wsgi.py process-group=django

Alias /time/static/ /var/www/html/time_app/static/ 
<Directory /var/www/html/time_app/static/>
      Require all granted
</Directory>
```
