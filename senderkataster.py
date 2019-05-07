#!/usr/bin/env python3

import requests
import pprint
import json
import time

pp = pprint.PrettyPrinter(indent=4)

# this should encompass all the points
bounds = [
  ('bounds[]', '18.0'),
  ('bounds[]', '46.0'),
  ('bounds[]', '8.0'),
  ('bounds[]', '49.0'),
]

r = requests.post('https://www.senderkataster.at/data/getPoints', data=bounds)
r.raise_for_status()

data = r.json()

# write the parsed data to a file, we store it in git to get the diffs
with open('points.json', 'w') as f:
    f.write(json.dumps(data, indent=4, sort_keys=True))

for point in data:
    params = {'layer': point['layer'], 'senderId': point['sender_id']}
    r = requests.post('https://www.senderkataster.at/data/getDetails', data=params)
    r.raise_for_status()
    data = r.json()

    # pretend we're a flat file database
    with open('senders/' + point['sender_id'] + '.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

    time.sleep(0.01) # let's try to be nice and only do 10rps
