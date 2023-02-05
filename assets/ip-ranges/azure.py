#!/usr/bin/python3

import json
from collections import defaultdict

with open("azure-ip-ranges.json", "r") as f:
    azure_ips = json.load(f)

ranges = defaultdict(list)

for range in azure_ips["values"]:
    rid = range["id"]
    properties = range["properties"]
    pregion = properties["region"]
    if pregion:
        # print(rid, pregion)
        # print(properties["regionId"], properties["addressPrefixes"])
        ranges[pregion].extend(properties["addressPrefixes"])
        # ranges.append((properties["region"], properties["addressPrefixes"]))

mapping = {}

for region_name in list(ranges.keys()):
    climatiq_name = input(f"{region_name}: ")
    mapping[region_name] = climatiq_name

print(mapping)

# for rid, ips in ranges:
#     if rid == "westus":
#         print(ips)
