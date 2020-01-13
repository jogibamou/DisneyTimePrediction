import json
import csv
import glob

air_quality_dict = {}

files = glob.glob('airdata/*.csv')

for file in files:
    print("Parsing data in ", file, "....")
    with open(file) as Data:
        csvr = csv.reader(Data)
        for row in csvr:
            if row[0] not in air_quality_dict:
                air_quality_dict[row[0]] = {"data": []}
            air_quality_dict[row[0]]['data'].append({
                'CSBA Code': row[1],
                'Date': row[2],
                'AQI': row[3],
                'Category': row[4],
                'Defining Parameter': row[5],
                'Number of Sites Reporting': row[6]
            })

air_quality_dict.pop("CBSA", None)

print("Processing completed.")
print("Converting to json...")
with open('daily_air_quality_data.json', 'w') as writefile:
    json.dump(air_quality_dict, writefile, indent=4)
print("Process Completed.")

