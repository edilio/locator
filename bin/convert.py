#!/usr/bin/env python
import os
import sys

#
APP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(APP_DIR)
sys.path.append(os.path.dirname(APP_DIR))
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locator.settings')

import django
django.setup()

from properties.models import *
import timeit

#counties = County.objects.all()
#for county in counties:
#    county.save(using='sqlite')


def save_to_sql(model):
    lst = model.objects.all()
    print "converting %s len: %d" %(model._meta.db_table,len(lst))
    for obj in lst:
        print obj.__unicode__()
        obj.save(using='mysql')


def save_all():
    models = [County, City, Owner, ManagementAgent, Property]
    for model in models:
        save_to_sql(model)


def print_all(db):
    models = [County, City, Owner, ManagementAgent, Property]

    for model in models:
        lst = model.objects.using(db).all()
        print "converting %s len: %d" %(model._meta.db_table,len(lst))
        for obj in lst:
            print obj.__unicode__()
        #save_to_sql(model)


def printsqlite():
    print_all('sqlite')


def printsqlserver():
    print_all('sqlserver')


def printmysql():
    print_all('default')


t = timeit.Timer(stmt=printsqlite)
lite = t.timeit(number=1)
print "%.2f usec/pass using sqlite" % lite


t = timeit.Timer(stmt=printmysql)
mysql = t.timeit(number=1)
print "%.2f usec/pass using mysql" % mysql


t = timeit.Timer(stmt=printsqlserver)
sqlserver = t.timeit(number=1)
print "%.2f usec/pass using sqlserver" %sqlserver


print "%.2f in sqlite, %.2f in mysql, %.2f in sqlserver" %(lite, mysql, sqlserver)
##87.62 usec/pass using sqlserver
##83.04 usec/pass using mysql
##82.09 usec/pass using sqlite

print 'done!!!'