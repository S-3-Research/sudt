import time
import googlemaps
import json
import pickle
import os
from tqdm import tqdm

# Replace with your own API key
API_KEY = 'AIzaSyDS2MjxY0euG-OXPvtu53zvjG7CWxAzKJE'
time_gap = 2
max_pages = 100
# data_dir = f"data/050523"

# Create a client with your API key
gmaps = googlemaps.Client(key=API_KEY)
place_details = []
for treatment_center in json.load(open("treatment_center_places_(42.361145, -71.057083).json", "r"))[:5]:
    response = gmaps.place(place_id=treatment_center["place_id"], language='en-US')
    place_details.append(response["result"])
    time.sleep(time_gap)

json.dump(place_details, open("treatment_center_place_details_42.361145,-71.057083.json", "w"))