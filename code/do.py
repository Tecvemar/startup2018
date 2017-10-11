# -*- encoding: utf-8 -*-
#~ x = raw_input('Favor DETENER el servidor Open y pgadmin para comenzar y pulse [Enter]...')
#~ import start
#~ x = raw_input('Favor INICIAR el servidor OpenERP para continuar y pulse [Enter]...')
#~ import load_common_data
x = raw_input('Favor DETENER el servidor Open y pgadmin para continuar y pulse [Enter]...')
import backup_bdd_ref
import create_bdd_companies
x = raw_input('Favor INICIAR el servidor OpenERP para continuar y pulse [Enter]...')
import load_companies_data
