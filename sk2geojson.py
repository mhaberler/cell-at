#!/usr/bin/env python3


import json
import pyproj
import geojson


proj = pyproj.Transformer.from_crs(3857, 4326, always_xy=True)

with open("points.json", "rb") as f:
    points = json.loads(f.read())


fc = geojson.FeatureCollection([])

for s in points["data"]:
    if not s['x'] or not s['y']:
        continue
    senderId = s['sender_id']

    with open(f'senders/{senderId}.json', 'r') as d:
        props = json.loads(d.read())
    lon, lat = proj.transform(float(s['x']), float(s['y']))
    f = geojson.Feature(
                geometry=geojson.Point((lon, lat)), properties=props[0]
            )
    fc.features.append(f)

with open('points.geojson', 'wb') as gj:
    gj.write(geojson.dumps(fc, indent=4).encode("utf-8"))

