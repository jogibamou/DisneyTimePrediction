CREATE TABLE "Warehouse".weather_data
(
	dataid integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	station_name varchar(64) NOT NULL,
	date timestamp NOT NULL,
	precipitation numeric,
	temp_avg numeric,
	temp_max numeric,
	temp_min numeric
)
