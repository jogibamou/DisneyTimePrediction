CREATE TABLE "Warehouse"."Attractions"
(
	AttractionID INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
	Name VARCHAR(128) NOT NULL,
	ParkID INT NOT NULL REFERENCES "Warehouse"."Parks"(ParkID),
	Notes VARCHAR(128) NULL
)