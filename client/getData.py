import json, pathlib
from tqdm import tqdm

HOME = pathlib.Path(__file__).parent.absolute()

v4_ranges = {}
v4_cpu_ranges = {}
v6_ranges = {}
v6_cpu_ranges = {}

services = {"amazon": "aws", "google": "gcp", "azure": "azure"}
ipv4_fmt = {"amazon": "ip_prefix", "google": "ipv4Prefix", "azure": "addressPrefix"}
ipv6_fmt = {"amazon": "ipv6_prefix", "google": "ipv6Prefix", "azure": "addressPrefix"}
scope_fmt = {"aws": "region", "gcp": "scope", "azure": ""}


def get_co2(service, scope):
    fileEnd = scope.replace("-", "_")
    path = HOME / f"../assets/networking-emissions/{service}/{service}-{fileEnd}.json"
    if path.exists():
        with open(path, "r") as file:
            data = json.load(file)
            return data["co2e"]
    else:
        return None

def get_cpu(service, scope):
    fileEnd = scope.replace("-", "_")
    path = HOME / "../assets/cpu-emissions/{service}_lookup.json"
    if path.exists():
        with open(path, "r") as file:
            data = json.load(file)
            return data[fileEnd]
    else:
        return None
        

for name in ["aws", "azure", "gcp"]:
    d = {}
    with open(HOME / f"../assets/cpu-emissions/{name}_cpu.json", "r") as file:
        data = json.load(file)
        for result in data["results"]:
            d[result["emission_factor"]["id"]] = result["co2e"]
    json.dump(d, open(HOME / f"../assets/cpu-emissions/{name}_lookup.json", "w"))        

for name in ["amazon", "google"]:
    with open(HOME / f"../assets/ip-ranges/{name}-ip-ranges.json", "r") as file:
        data = json.load(file)
        for prefix in tqdm(data["prefixes"] + data.get("ipv6_prefixes", [])):
            if ipv4_fmt[name] in prefix:
                v4_cpu_ranges[prefix[ipv4_fmt[name]]] = get_cpu(
                    services[name], prefix[scope_fmt[services[name]]]
                )
            else:  # ipv6
                v6_cpu_ranges[prefix[ipv6_fmt[name]]] = get_cpu(
                    services[name], prefix[scope_fmt[services[name]]]
                )

for name in ["amazon", "google"]:
    with open(HOME / f"../assets/ip-ranges/{name}-ip-ranges.json", "r") as file:
        data = json.load(file)
        for prefix in tqdm(data["prefixes"] + data.get("ipv6_prefixes", [])):
            if ipv4_fmt[name] in prefix:
                v4_ranges[prefix[ipv4_fmt[name]]] = get_co2(
                    services[name], prefix[scope_fmt[services[name]]]
                )
            else:  # ipv6
                v6_ranges[prefix[ipv6_fmt[name]]] = get_co2(
                    services[name], prefix[scope_fmt[services[name]]]
                )

# Map from the region naming scheme used by the Azure IPs JSON file from Microsoft to the region names used in our Climatiq dataset
AZURE_MAP = {
    "australiacentral": "australia_central",
    "australiacentral2": "australia_central_2",
    "australiaeast": "australia_east",
    "australiasoutheast": "australia_south_east",
    "brazilsouth": "brazil_south",
    "brazilse": "brazil_south_east",
    "canadacentral": "canada_central",
    "canadaeast": "canada_east",
    "centralindia": "central_india",
    "centralus": "central_us",
    "centraluseuap": "central_us",
    "eastasia": "east_asia",
    "eastus": "east_us",
    "eastus2": "east_us_2",
    "eastus2euap": "east_us_2",
    "centralfrance": "france_central",
    "southfrance": "france_south",
    "germanyn": "germany_north",
    "germanywc": "germany_west_central",
    "japaneast": "japan_east",
    "japanwest": "japan_west",
    "jioindiacentral": "india_central",
    "jioindiawest": "india_west",
    "koreacentral": "korea",
    "northcentralus": "north_central_us",
    "northeurope": "north_europe",
    "norwaye": "norway_east",
    "norwayw": "norway_west",
    "qatarcentral": "united_arab_emirates",
    "southafricanorth": "south_africa_north",
    "southafricawest": "south_africa_west",
    "southcentralus": "south_central_us",
    "southindia": "south_india",
    "southeastasia": "southeast_asia",
    "swedencentral": "sweden_central",
    "swedensouth": "sweden_central",
    "switzerlandn": "switzerland_north",
    "switzerlandw": "switzerland_west",
    "uaecentral": "united_arab_emirates_central",
    "uaenorth": "united_arab_emirates_north",
    "uknorth": "uk",
    "uksouth": "uk_south",
    "uksouth2": "uk_south",
    "ukwest": "uk_west",
    "westcentralus": "west_central_us",
    "westeurope": "west_europe",
    "westindia": "west_india",
    "westus": "west_us",
    "westus2": "west_us_2",
    "westus3": "west_us_3",
    "koreasouth": "korea_south",
    "usstagec": "central_us",
    "brazilne": "brazil",
    "northeurope2": "north_europe",
}

with open(HOME / "../assets/ip-ranges/azure-ip-ranges.json", "r") as file:
    azure_ips = json.load(file)
    for range in tqdm(azure_ips["values"]):
        properties = range["properties"]
        region = properties["region"]
        if not region:
            continue
        climatiq_region = AZURE_MAP[region]
        v4_ranges.update(
            {
                prefix: get_co2("azure", climatiq_region)
                for prefix in properties["addressPrefixes"]
                if "::" not in prefix
            }
        )
        v6_ranges.update(
            {
                prefix: get_co2("azure", climatiq_region)
                for prefix in properties["addressPrefixes"]
                if "::" in prefix
            }
        )

json.dump(v4_ranges, open(HOME / "../assets/all-ranges.json", "w"))
json.dump(v4_cpu_ranges, open(HOME / "../assets/all_cpu-ranges.json", "w"))
json.dump(v6_ranges, open(HOME / "../assets/v6-ranges.json", "w"))
json.dump(v6_cpu_ranges, open(HOME / "../assets/v6_cpu-ranges.json", "w"))
