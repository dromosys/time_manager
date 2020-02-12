FROM debian

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install python-pip apache2 libapache2-mod-wsgi-py3
RUN apt-get -y install python3 python3-virtualenv

RUN pip install --upgrade pip
RUN pip install djangorestframework
ADD webapp/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install django
ADD webapp/demo_site.conf /etc/apache2/sites-available/000-default.conf
ADD webapp /var/www/html
RUN chmod 664 /var/www/html/db/db.sqlite3
RUN chmod 775 /var/www/html/db
RUN chown :www-data -R /var/www/html/db/db.sqlite3
RUN chown :www-data -R /var/www/html/db
RUN cd /var/www/html; python manage.py makemigrations; python manage.py migrate

EXPOSE 80
CMD apachectl -D FOREGROUND
