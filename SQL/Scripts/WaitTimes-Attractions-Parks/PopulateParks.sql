INSERT INTO "Warehouse"."Parks" ("name", "locationid") 
SELECT "parkname", 0 FROM "Warehouse"."AttractionWaitTimesBuffer" as buffer
LEFT JOIN "Warehouse"."Parks" AS parks
ON
parks."name" = buffer."parkname"
WHERE 
parks."name" is NULL 
GROUP BY buffer."parkname";

