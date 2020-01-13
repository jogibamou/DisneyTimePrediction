INSERT INTO "Warehouse"."AttractionWaitTimes" ("attractionid", "timestamp", "waittime")
SELECT "attractions"."attractionid", "timestamp", "waittime"
FROM "Warehouse"."AttractionWaitTimesBuffer" AS buffer
INNER JOIN "Warehouse"."Attractions" AS attractions
ON 
"buffer"."attractionname" = "attractions"."name"
LEFT JOIN "Warehouse"."AttractionWaitTimes" AS waittimes
ON
"waittimes"."attractionid" = "attractions"."attractionid" AND "waittimes"."timestamp" = "buffer"."timestamp"
WHERE
"waittimes"."dataid" is NULL;