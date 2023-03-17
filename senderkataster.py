#!/usr/bin/env python3

import requests
import json
import time
from tqdm import tqdm

r = requests.post('https://www.senderkataster.at/backend//data/getconfig.php') 
r.raise_for_status()
data = json.loads(r.content)

# write the parsed data to a file, we store it in git to get the diffs
with open('points.json', 'w') as f:
    f.write(json.dumps(data, indent=4, sort_keys=True))

for point in tqdm(data['data']):
    layer =  point['layer']
    senderId =  point['sender_id']
    # print(layer, senderId)
    # continue

    r = requests.post(f'https://www.senderkataster.at/backend/data/getdetails.php?layer={layer}&sender_id={senderId}')
    r.raise_for_status()
    data = json.loads(r.content)

    # pretend we're a flat file database
    with open(f'senders/{senderId}.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

    time.sleep(0.01) # let's try to be nice and only do 10rps
