from DatasetAPI import Datasets

data = Datasets.DataAccessor()

# Get and print the first thousand rows of air_quality_buffer
rows = data.get('Warehouse', 'Attractions', limit = 100)

print(rows[0])
print(rows[0][2])