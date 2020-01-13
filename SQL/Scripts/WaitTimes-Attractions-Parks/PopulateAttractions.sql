INSERT INTO "Warehouse"."Attractions" ("name", "parkid")
SELECT "attractionname", parks."parkid"
FROM "Warehouse"."AttractionWaitTimesBuffer" as buffer 
INNER JOIN "Warehouse"."Parks" as parks
ON
	parks."name" = buffer."parkname"
LEFT JOIN "Warehouse"."Attractions" AS attractions 
ON 
	attractions."name" = buffer."attractionname" 
WHERE 
	parks."name" = buffer."parkname" AND attractions."name" is NULL
GROUP BY buffer."attractionname", parks."parkid";

SELECT * FROM "Warehouse"."Attractions";