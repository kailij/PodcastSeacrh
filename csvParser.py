import csv
import json

csvFilePath = "./poddf.csv"
jsonFilePath = "./dataset.json"

data = []
# Read the csv file and add the data to a dictionary
with open(csvFilePath, encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    print("start")

    docId = 0

    for row in reader:
        # put an id key value pair
        row.update({"docId": str(docId)})
        row.move_to_end("docId", last=False)

        # remove original index
        del row["index"]

        # replace \n with whitespace
        for key, value in row.items():
            value = value.replace('\n', ' ')
            # replace "NOT_FOUND" value with "0"
            if key == "Rating_Volume" or key == "Rating":
                if value == "Not Found":
                    value = 0.00
                else:
                    value = float(value)
            row[key] = value
        # put raw content to data list
        data.append(row)
        docId += 1
        print(docId)

# Write data to a JSON file
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(data))
    print("finish")
