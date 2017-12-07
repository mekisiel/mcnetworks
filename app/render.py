from jinja2 import Environment, FileSystemLoader
from netaddr import IPNetwork

def gateway(input):
    network = IPNetwork(input)
    gateway = str(network[1])
    return gateway

def dotmask(input):
    network = IPNetwork(input)
    dotmask = str(network.netmask)
    return dotmask

def render(action, variables):
    # Start manipulation of input variables to format for netaddr filters
    variables['network_'] = str(variables['network'] + '/' +  str(variables['mask']))
    # End manipulation of input variables to format for netaddr filters
    loader = FileSystemLoader('./templates')
    jenv = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    jenv.filters['gateway'] = gateway
    jenv.filters['dotmask'] = dotmask
    template = jenv.get_template(action + '.j2')
    config = (template.render(variables))
    with open('./staging/' + action + '.conf', 'w') as output:
        output.write(config)
    print('\t''Configuration built')
