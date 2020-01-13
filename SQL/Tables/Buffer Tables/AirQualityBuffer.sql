CREATE TABLE "Warehouse".air_quality_buffer
(
	location_name varchar(128) NOT NULL,
	csba_code varchar(32),
	date date NOT NULL,
	aqi int,
	category varchar(32),
	defining_parameter varchar(32)
)