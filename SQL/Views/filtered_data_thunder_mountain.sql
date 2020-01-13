CREATE OR REPLACE VIEW filtered_data_thunder_mountain
AS
SELECT
	timestamp,
	EXTRACT(MONTH FROM fwt.timestamp) AS month,
	EXTRACT(dow FROM fwt.timestamp) AS dow,
	EXTRACT(HOUR FROM fwt.timestamp) AS hour,
	fwd.precipitation,
	fwd.temp_avg,
	fwd.temp_max,
	fwd.temp_min,
	fwt.waittime
FROM 
	filtered_wait_times_nonrandom as fwt
INNER JOIN flattened_weather_data AS fwd
ON
	fwt.timestamp::date = fwd.date::date
INNER JOIN filtered_attractions AS fa
ON
	fwt.attractionid = fa.attractionid
WHERE
	fa.attractionid = 213 -- thunder mountain attractionID
ORDER BY random();