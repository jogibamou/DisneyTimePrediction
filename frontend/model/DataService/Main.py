import Service
import time
from Config import Config
from Data import DataRepository

def main():
	config = Config.Config()
	print("Config loaded")
	max_rows_per_insert = 10000
	repo = DataRepository.DataRepository(config.db_info, max_rows_per_insert)
	print(repo.test_connection())

	delay = 60 * 15 # Make requests every fifteen minutes 

	while True:
		Service.GetWaitData(repo)
		time.sleep(delay)


if __name__ == "__main__":
	main()