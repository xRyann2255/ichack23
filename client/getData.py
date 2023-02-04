import json, pathlib
HOME = pathlib.Path(__file__).parent.absolute()

with open(HOME/'../assets/ip-ranges/amazon-ip-ranges.json', 'r') as file:
    data = json.load(file)

amazon_ip_ranges = [prefix['ip_prefix'] for prefix in data['prefixes']]
print(amazon_ip_ranges)