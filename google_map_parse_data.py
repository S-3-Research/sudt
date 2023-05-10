import os
import json
import pandas as pd
from geojson import Feature, Point, FeatureCollection, dump

data_dir = "data/050523"

treatment_centers = []
for file in os.listdir(data_dir):
    if file.startswith("treatment_center_places_"):
        print(file)
        treatment_centers += json.load(open(f"{data_dir}/{file}", "r"))
print(f"Total treatment centers: {len(treatment_centers)}")


treatment_centers = list({x["place_id"]: x for x in treatment_centers}.values())
print(f"Unique treatment centers: {len(treatment_centers)}")

treatment_centers = list(filter(lambda x: x["formatted_address"].endswith("United States"), treatment_centers))
print(f"Unique treatment centers in US: {len(treatment_centers)}")

def parse_treatment_center(treatment_center):
    return {
        "place_id": treatment_center["place_id"],
        "name": treatment_center["name"],
        "address": treatment_center["formatted_address"],
        "latitude": treatment_center["geometry"]["location"]["lat"],
        "longitude": treatment_center["geometry"]["location"]["lng"],
        "types": treatment_center["types"],
        "rating": treatment_center["rating"],
        "user_ratings_total": treatment_center["user_ratings_total"],
        "business_status": treatment_center["business_status"],
    }

treatment_centers = list(map(parse_treatment_center, treatment_centers))
pd.DataFrame.from_records(treatment_centers).to_csv("treatment_centers.csv", index=False)

features = [Feature(geometry=Point([x["longitude"], x["latitude"]])) for x in treatment_centers]
dump(FeatureCollection(features), open("treatment_centers.geojson", "w"))