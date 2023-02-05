import json, pathlib
from tqdm import tqdm
HOME = pathlib.Path(__file__).parent.absolute()

v4_ranges = {}
v6_ranges = {}

services = {'amazon':'aws','google':'gcp','azure':'azure'}
ipv4_fmt = {'amazon':'ip_prefix','google':'ipv4Prefix','azure':'addressPrefix'}
ipv6_fmt = {'amazon':'ipv6_prefix','google':'ipv6Prefix','azure':'addressPrefix'}
scope_fmt = {'aws':'region','gcp':'scope','azure':''}

def get_co2(service,scope):
    fileEnd = scope.replace('-', '_')
    path = HOME/f'../assets/networking-emissions/{service}/{service}-{fileEnd}.json'
    if path.exists():
        with open(HOME/f'../assets/networking-emissions/{service}/{service}-{fileEnd}.json', 'r') as file:
            data = json.load(file)
            return data["co2e"]
    else:
        return None


for name in ['amazon','google']:
    with open(HOME/f'../assets/ip-ranges/{name}-ip-ranges.json', 'r') as file:
        data = json.load(file)
        for prefix in tqdm(data["prefixes"]+data.get("ipv6_prefixes",[])):
            if ipv4_fmt[name] in prefix:
                v4_ranges[prefix[ipv4_fmt[name]]] = get_co2(services[name],prefix[scope_fmt[services[name]]])
            else: #ipv6
                v6_ranges[prefix[ipv6_fmt[name]]] = get_co2(services[name],prefix[scope_fmt[services[name]]])


# TODO: azure

json.dump(v4_ranges, open(HOME/'../assets/all-ranges.json', 'w'))
json.dump(v6_ranges, open(HOME/'../assets/v6-ranges.json', 'w'))
