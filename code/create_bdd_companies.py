#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from definitions import dbdata

con = connect(host=dbdata['host'], dbname='postgres',
              user=dbdata['postgresql_login'],
              password=dbdata['postgresql_password'])

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

for db in dbdata['databases'][2:3]:
    dbdata.update({'database_name': db})

    try:
        print """DROP DATABASE %(database_name)s""" % dbdata
        cur.execute("""DROP DATABASE %(database_name)s;""" % dbdata)
    except:
        pass

    print """CREATE DATABASE %(database_name)s""" % dbdata
    cur.execute("""CREATE DATABASE %(database_name)s
                     WITH OWNER = %(postgresql_login)s
                          ENCODING = 'UTF8'
                          TABLESPACE = pg_default
                          LC_COLLATE = 'es_VE.UTF-8'
                          LC_CTYPE = 'es_VE.UTF-8'
                          CONNECTION LIMIT = -1;""" % dbdata)

    restore = ('/usr/bin/pg_restore --host localhost --port 5432 ' +
               '--username "%(postgresql_login)s" ' +
               '--dbname "%(database_name)s" --no-password ' +
               '--verbose "%(backup_file)s"') % dbdata
    print """RESTORE DATABASE %(database_name)s""" % dbdata
    os.system(restore)
