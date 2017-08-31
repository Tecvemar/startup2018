# -*- encoding: utf-8 -*-
import os
from definitions import dbdata

print 'Respaldando Bdd...'

backup = ('/usr/bin/pg_dump --host localhost --port 5432 ' +
          '--username "%(postgresql_login)s" --no-password  ' +
          '--format custom --blobs --verbose --file "%(backup_file)s" ' +
          '"%(dbgen)s"') % dbdata
print backup
print """BACKUP DATABASE %s""" % dbdata['dbgen']
os.system(backup)
