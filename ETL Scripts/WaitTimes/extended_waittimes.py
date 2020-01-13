import csv
from DataRepository import DataRepository
from Config import Config
def getint(val):
    try:
        val = int(val)
        return int(val)
    except ValueError:
        return -999

data = []
attraction_num = 252     
timestamp_index = 1
first_wait_time_index = 2
second_wait_time_index = 3

csvfile = open('splash_mountain.csv', newline='')

reader = csv.reader(csvfile, delimiter=',')

for row in reader:
    data.append((attraction_num, row[1], max(getint(row[2]), getint(row[3]))))


repo = DataRepository(Config().db_info ,10000)
queries = repo.format_extended_wait_time_data(data[1:])

for query in queries:
    repo.execute_query(query)

