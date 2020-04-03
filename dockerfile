FROM debian

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev

RUN cd /usr/local/bin && ln -s /usr/bin/python3 python
RUN pip3 install --upgrade pip

RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install apache2 libapache2-mod-wsgi-py3

ADD requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ADD apache2.conf /etc/apache2/sites-available/000-default.conf
ADD . /var/www/html

RUN cd /var/www/html; python manage.py makemigrations; python manage.py migrate; python manage.py collectstatic --no-input
RUN chown :www-data -R /var/www/html/db/db.sqlite3
RUN chown :www-data -R /var/www/html/
RUN chmod 664 /var/www/html/db/db.sqlite3
RUN chmod 775 /var/www/html/db

EXPOSE 80
CMD apachectl -D FOREGROUND