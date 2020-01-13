CREATE TABLE "Warehouse".weather_data2
(
	dataid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	timestamp timestamp WITH TIME ZONE,
	temp numeric,
	temp_min numeric,
	temp_max numeric,
	pressure numeric,
	humidity numeric, 
	wind_speed numeric,
	weather_main varchar(128),
	weather_description varchar(128)
)

