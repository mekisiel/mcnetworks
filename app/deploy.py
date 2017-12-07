from napalm import get_network_driver
from os import path
import secrets

def deploy(action):
    hostname = '172.16.99.11'
    username = secrets.username
    password = secrets.password
    platform = 'ios'
    config = './staging/' + action + '.conf'
    driver = get_network_driver(platform)
    connect_handler = driver(hostname, username, password)
    if not (path.exists(config) and path.isfile(config)):
        msg = 'Missing or invalid config file {}'.format(config)
        raise ValueError(msg)
    connect_handler.open()
    connect_handler.load_merge_candidate(config)
    connect_handler.commit_config()
    connect_handler.close()
    print('\t''Configuration deployed')
