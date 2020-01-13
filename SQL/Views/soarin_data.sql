CREATE MATERIALIZED VIEW soarin_data
AS
SELECT
    awt.timestamp,
    awt.waittime,
    EXTRACT(MONTH FROM awt.timestamp) AS month,
    EXTRACT(dow FROM awt.timestamp) AS dow,
    EXTRACT(HOUR FROM awt.timestamp) AS hour,
    d2.temp,
    d2.temp_min,
    d2.temp_max,
    d2.pressure,
    d2.humidity,
    d2.wind_speed,
    CASE
           WHEN d2.weather_main::text = ANY (ARRAY['Rain'::character varying, 'Thunderstorm'::character varying]::text[]) THEN d2.weather_description
        ELSE d2.weather_main
    END AS weather_category,
	disney_volume,
	disney_open,
	disney_closed,
	disney_high,
	disney_low,
	sp_500,
	dow_jones
FROM 
    "Warehouse"."AttractionWaitTimesExpanded" AS awt
INNER JOIN "Warehouse"."weather_data2" AS d2
ON
	awt."timestamp"::date - make_interval(hours => date_part('hour'::text, awt."timestamp")::integer) = d2."timestamp"
LEFT JOIN "Warehouse".condensed_stock_prices AS sp
ON
	awt."timestamp"::date = sp."date"
WHERE
    awt.waittime >= 0 
	AND 
	awt.timestamp > '2013-01-02 21:00:00'

ORDER BY 
	awt.timestamp

