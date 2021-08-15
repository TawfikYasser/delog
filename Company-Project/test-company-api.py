import requests
import json

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/getcompanies/")
print(f"STATUS CODE: {response.status_code}")
print(f"CONTENT-TYPE: {response.headers['Content-Type']}")
print(f"DATA: {response.json()}")
with open("companies-data-serialize.json","w") as json_file:
    json.dump(response.json(),json_file)