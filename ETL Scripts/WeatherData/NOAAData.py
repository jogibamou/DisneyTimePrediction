import json
import csv
import glob


def main():
        stations = []
        csv_list= glob.glob("csvFiles/*.csv")
        json_path = "NOAAData.json"
        jsformat = ''
        
        print("Collecting data from CSV...\n")
        for csv_path in csv_list:
                stations.extend(read_csv(csv_path))

        print("Data collection complete.\n")

        print("Creating JSON file...\n")

        write_json(stations, json_path, jsformat)
        print("JSON file creation complete\n")


def read_csv(csv_path):
        stations = []
        data = []

        with open(csv_path) as csvfile:
                reader = csv.DictReader(csvfile)
                title = reader.fieldnames

                for row in reader:

                        data.append({'STATION':row['STATION'], 'DATA':{title[count]:row[title[count]] for count in range(5, len(title))}})

                        if (not contains(stations, row['STATION'])):
                                stations.append({'STATION':row['STATION'], 'NAME':row['NAME'], 'LOCATION':{'LONGITUDE':row['LONGITUDE'], 'LATITUDE':row['LATITUDE'], 'ELEVATION':row['ELEVATION']}})

                for i in stations:
                        i.update({'DATA':[]})
                        for j in data:
                                if (j['STATION'] == i['STATION']):
                                        i['DATA'].append(j['DATA'])

        
        return stations

def contains(stations, target):
        flag = False
        for obj in stations:
              if(target==obj['STATION']):
                      flag = True
        return flag   


def write_json(data, json_file, format):
        with open(json_file, "w") as f:
                if format == 'pretty':
                        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '),encoding="utf-8",ensure_ascii=False))
                else:
                        f.write(json.dumps(data))



if __name__ == "__main__":
   main()