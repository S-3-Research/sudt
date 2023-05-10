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

# Define the search parameters
search_query = 'treatment center'
locations = [(42.361145, -71.057083)]
# locations = json.load(open(f"{data_dir}/coordinates_contiguous_us.json", "r"))

for location in tqdm(locations[:], desc="Locations"):
    # visited = json.load(open(f"{data_dir}/visited.json", "r")) if os.path.exists(f"{data_dir}/visited.json") else {}
    location = tuple(location)

    # Perform the search
    treatment_centers = []
    response = gmaps.places(query=search_query, location=location, language='en-US', type='health', radius = 50000)
    treatment_centers += response['results']
    time.sleep(time_gap)    

    # Fetch additional pages of results, up to a maximum of x pages
    num_pages = 1
    while 'next_page_token' in response and num_pages < 100:
        # print(response['next_page_token'])
        # Send a text search request to the Google Maps API for the next page of results
        response = gmaps.places(query=search_query, page_token=str(response['next_page_token']))
        treatment_centers += response['results']
        time.sleep(time_gap)    
        num_pages += 1

    json.dump(treatment_centers, open(f"treatment_center_places_{location}.json", "w"))
    # Print the results
    # json.dump(treatment_centers, open(f"{data_dir}/treatment_center_places_{location}.json", "w"))
    # visited[str(location)] = {"num_calls": num_pages, "num_results": len(treatment_centers)}
    # json.dump(visited, open(f"{data_dir}/visited.json", "w"))