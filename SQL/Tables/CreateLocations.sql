CREATE TABLE "Warehouse"."Locations"
(
	LocationID INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
	City varchar(128) NULL,
	County varchar(128) NULL,
	State varchar(64) NOT NULL,
	Zip varchar(32) NOT NULL,
	Timezone int NOT NULL,
	Longitude DECIMAL(16),
	Latitude DECIMAL(16)
)