CREATE VIEW filtered_air_quality_data AS
SELECT 
	"date",
	"aqi",
	"category",
	"defining_parameter"
FROM "Warehouse"."air_quality_buffer"
WHERE "location_name" = 'Orlando-Kissimmee-Sanford,FL';
	