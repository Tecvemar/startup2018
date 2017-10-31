# -*- encoding: utf-8 -*-
import os
from definitions import dbdata

for database in dbdata['databases'][:6]:
    print 'Respaldando Bdd %s...' % database
    bkdata = {
        'backup_file': '../data/companies/%s.backup' % database,
        'database': database,
        'postgresql_login': dbdata['postgresql_login']
        }

    backup = ('/usr/bin/pg_dump --host localhost --port 5432 ' +
              '--username "%(postgresql_login)s" --no-password  ' +
              '--format custom --blobs --verbose --file "%(backup_file)s" ' +
              '"%(database)s"') % bkdata
    #~ print backup
    #~ print """BACKUP DATABASE %s""" % database
    os.system(backup)
