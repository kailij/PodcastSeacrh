from elasticsearch import Elasticsearch
import json

es = Elasticsearch()
# every time before use, clear index=="podcast-index" in elasticsearch
es.indices.delete(index='podcast-index', ignore=[400, 404])

# index mappings rules
mappings_setting = {
    "mappings": {
        "properties": {
            "docId": {"type": "text"},
            "Name": {"type": "text"},
            "Rating_Volume": {"type": "text"},
            "Rating": {"type": "text"},
            "Genre": {"type": "text"},
            "Description": {"type": "text"},
        }
    }
}

# create index
es.indices.create(index="podcast-index", body=mappings_setting)

# write each record into elastic as a json object
jsonFilePath = "./dataset.json"
try:
    # Write data to a JSON file
    with open(jsonFilePath) as jsonFile:
        data = json.load(jsonFile)  # data list
        print("Start to load data")

        for item in data:
            es.index(index="podcast-index", body=item, id=item["docId"])
            print("loading..." + item["docId"])
except Exception as e:
    print(e)

print("Finish load data")



