CREATE TABLE "Warehouse"."AttractionWaitTimes"
(
	DataID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	AttractionID INT NOT NULL REFERENCES "Warehouse"."Attractions"(AttractionID),
	Timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
	WaitTime INT NOT NULL,
	CONSTRAINT unique_data UNIQUE(AttractionID, Timestamp)
)