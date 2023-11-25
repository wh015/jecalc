#!/usr/bin/python3

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help = "Input JSON file", required = True)
args = parser.parse_args()

f = open(args.input)
data = json.load(f)
f.close


consumers = {}
shared = 0.0
total = 0.0

for item in data["items"]:
    clen = 0
    count = 1
    price = item["price"]

    if "consumers" in item:
        clen = len(item["consumers"])

    if clen == 0:
        shared += price
        continue

    if "count" in item:
        count = item["count"]
        price *= count

    for consumer in item["consumers"]:
        if consumer in consumers:
            consumers[consumer] += price / clen
        else:
            consumers[consumer] = price / clen

clen = len(consumers)
if clen > 0:
    shared /= clen


for consumer in consumers:
    consumers[consumer] = round(consumers[consumer] + shared, 2)
    total += consumers[consumer]
    print('{:<12}  {:>12.2f}'.format(consumer, consumers[consumer]))

print('\n{:<12}  {:>12.2f}'.format("Total", round(total, 2)))

