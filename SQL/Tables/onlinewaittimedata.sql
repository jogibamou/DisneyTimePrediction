CREATE TABLE sitedata.online_waittimes
(
	dataid int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	attractionid int REFERENCES "Warehouse"."Attractions"(attractionid),
	timestamp timestamp NOT NULL,
	waittime int NOT NULL
)