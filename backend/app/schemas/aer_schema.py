import json
import os

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "aer_schema.json")

with open(SCHEMA_PATH, "r") as f:
    schema = json.load(f)
