#!/bin/bash

/usr/bin/sudo /bin/su - amfoss
cd /var/www/cms
source bin/activate
/var/www/cms/bin/python manage.py log_status_updates --yesterday --send-telegram-report
