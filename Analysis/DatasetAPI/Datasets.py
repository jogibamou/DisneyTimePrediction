from Data import DataRepository
from Config import Config

rows_per_insert = 10000

# I stole the singleton-ness of this from stack overflow, no idea how it works
class Singleton(object):
	def __new__(self, *args, **kw):
		if not hasattr(self, '_instance'):
			orig = super(Singleton, self)
			self._instance = orig.__new__(self, *args, **kw)
		return self._instance

class DataAccessor(Singleton):
	def __init__(self):
		if not hasattr(self, 'repo'):
			config = Config.Config()
			self.repo = DataRepository.DataRepository(config.db_info, rows_per_insert)

	# Gets a dataset by the name of the associated object
	def get(self, schema_name, dataset_name, type=None, rows = '*', limit=1000):
		# If type = stored procedure then execute a stored procedure and get the results
		if(type=="sp"):
			raise exception("Stored procedures and table valued functions are currently not supported.")
		# Else, assume it's a table or view
		else:
			query = f'SELECT {rows} FROM "{schema_name}"."{dataset_name}" LIMIT {limit}'
		return self.repo.execute_query_return_rows(query)		