import requests
# import psycopg2
import datetime 
from datetime import timedelta

def GetWaitData(repo):
	# ### Constants
	url = "http://localhost"
	port = 3150
	endpoint = "waittime"

	# #### Get data from node server
	# First, get attractions to update
	attractions_raw = repo.execute_and_return("SELECT attractionid, name FROM \"Warehouse\".\"Attractions\" WHERE attractionid IN (248,246,209,215,220,238,245,251,252,213)")
	attractions = {}
	for row in attractions_raw:
		attractions[row[1]] = row[0]
	
	url = f"{url}:{port}/{endpoint}/"
	r = requests.get(url)
	d = r.json()
	data = []
	for attraction in attractions.keys():
		try:
			# EC2 uses utc so subtract five hours to force it to be EST
			# Really lazy 
			data.append([attractions[attraction], f'$${(datetime.datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")}$$', d[attraction.strip()]])
			print(f"{attraction} found!")
		except KeyError:
			print(f"not found: \"{attraction}\" ")
	print(f"Inserting rows: {data}")
	#### Insert into database
	columns = ['attractionid','timestamp','waittime']
	repo.insert_rows_into_table("online_waittimes", columns, data, "sitedata")
