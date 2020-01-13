CREATE OR REPLACE VIEW flattened_weather_data
AS
SELECT
	date,
	precipitation,
	temp_avg,
	temp_max,
	temp_min
FROM 
	"Warehouse"."weather_data"
WHERE
	station_name = 'ORLANDO INTERNATIONAL AIRPORT, FL US'
