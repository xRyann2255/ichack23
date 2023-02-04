import json, pathlib
from tqdm import tqdm
HOME = pathlib.Path(__file__).parent.absolute()

all_ranges = {}
services = {'amazon':'aws','google':'gcp','azure':'azure'}
ip_fmt = {'amazon':'ip_prefix','google':'ipv4Prefix','azure':'addressPrefix'}
scope_fmt = {'aws':'region','gcp':'scope','azure':''}

def get_co2(service,scope):
    fileEnd = scope.replace('-', '_')
    path = HOME/f'../assets/networking-emissions/{service}/{service}-{fileEnd}.json'
    if path.exists():
        with open(HOME/f'../assets/networking-emissions/{service}/{service}-{fileEnd}.json', 'r') as file:
            data = json.load(file)
            return data["co2e"]
    else:
        print(service, scope)


for name in ['amazon','google']:
    with open(HOME/f'../assets/ip-ranges/{name}-ip-ranges.json', 'r') as file:
        data = json.load(file)
        all_ranges.update({prefix[ip_fmt[name]]: get_co2(services[name],prefix[scope_fmt[services[name]]])
            for prefix in tqdm(data["prefixes"]) if ip_fmt[name] in prefix})

# TODO: azure

json.dump(all_ranges, open(HOME/'../assets/all-ranges.json', 'w'))
