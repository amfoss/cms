#!/bin/bash

/usr/bin/sudo /bin/su - amfoss
cd /var/www/cms
source bin/activate
/var/www/cms/bin/python manage.py create_daily_thread