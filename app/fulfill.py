from database import mod_db, search_db
from deploy import deploy
from render import render
from sys import argv

script, action, size, name, env, owner, index = argv

print('STARTING FULFILLMENT')
print('LOCATING NETWORK')
resource = search_db(action, size, name, env, index)
res_index = resource['id']
if action == 'add':
    print('CREATING NETWORK RESERVATION')
    resource_mod = mod_db(action, name, owner, res_index)
else:
    # action == 'delete'
    print('REMOVING NETWORK RESERVATION')
    resource_mod = mod_db(action, name, owner, res_index)
print('CREATING ' + action.upper() + ' CONFIGURATION')
variables = search_db(None, None, None, None, res_index)
render(action, variables)
print('DEPLOYING ' + action.upper() + ' CONFIGURATION')
deploy(action)
print('FINISHED FULFILLMENT')
