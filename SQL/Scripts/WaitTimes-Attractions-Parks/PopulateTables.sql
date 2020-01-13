INSERT INTO "Warehouse"."Parks" 
(
	"name", 
	"locationid"
) 
SELECT 
	"parkname", 
	3
FROM 
	"Warehouse"."AttractionWaitTimesBuffer" as buffer
LEFT JOIN "Warehouse"."Parks" AS parks
ON
	parks."name" = buffer."parkname"
WHERE 
	parks."name" is NULL 
GROUP BY 
	buffer."parkname";


INSERT INTO "Warehouse"."Attractions" 
(
	"name", 
	"parkid"
)
SELECT 
	"attractionname", 
	parks."parkid"
FROM 
	"Warehouse"."AttractionWaitTimesBuffer" as buffer 
INNER JOIN "Warehouse"."Parks" as parks
ON
	parks."name" = buffer."parkname"
LEFT JOIN "Warehouse"."Attractions" AS attractions 
ON 
	attractions."name" = buffer."attractionname" 
WHERE 
	parks."name" = buffer."parkname" AND attractions."name" is NULL
GROUP BY 
	buffer."attractionname", parks."parkid";


INSERT INTO 
	"Warehouse"."AttractionWaitTimes"
(
	"attractionid", 
	"timestamp", 
	"waittime"
)
SELECT 
	"attractions"."attractionid", 
	buffer."timestamp", 
	MAX(buffer."waittime")
FROM 
	"Warehouse"."AttractionWaitTimesBuffer" AS buffer
INNER JOIN "Warehouse"."Attractions" AS attractions
ON 	
	"buffer"."attractionname" = "attractions"."name"
LEFT JOIN "Warehouse"."AttractionWaitTimes" AS waittimes
ON
	"waittimes"."attractionid" = "attractions"."attractionid" AND "waittimes"."timestamp" = "buffer"."timestamp"
WHERE
	"waittimes"."dataid" is NULL
GROUP BY 
	"attractions"."attractionid", 
	buffer."timestamp";