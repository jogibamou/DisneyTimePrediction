CREATE TABLE "Warehouse".air_quality_categories
(
	categoryid INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
	categorylabel varchar(32) UNIQUE
)