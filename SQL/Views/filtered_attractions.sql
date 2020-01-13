CREATE VIEW filtered_attractions AS 
SELECT 
    "attractions"."attractionid",
    "attractions"."name", 
    "attractions"."parkid", 
    "attractions"."outdoor", 
    "attractions"."speed", 
    "attractions"."music", 
    "attractions"."dark",
    "attractions"."water", 
    "attractions"."coaster", 
    "attractions"."car", 
    "attractions"."train", 
    "attractions"."spinner", 
    "attractions"."isshow",
    "attractions"."story", 
    "attractions"."game", 
    "attractions"."simulation"
FROM 
    "Warehouse"."Attractions" AS attractions
LEFT JOIN "Warehouse"."AttractionWaitTimes" AS waittimes
ON
    "waittimes"."attractionid" = "attractions"."attractionid"
INNER JOIN 
    (
        SELECT "attractions"."attractionid" FROM "Warehouse"."Attractions" AS attractions
        LEFT JOIN "Warehouse"."AttractionWaitTimes" AS waittimes
        ON
        "waittimes"."attractionid" = "attractions"."attractionid"
        WHERE "waittimes"."waittime" > 0
        GROUP BY "attractions"."attractionid"
        HAVING COUNT("attractions"."attractionid") > 9315
    ) 
    AS Subquery
ON
    "attractions"."attractionid" = subquery.attractionid
WHERE "waittimes"."waittime" >= 0 
GROUP BY "attractions"."attractionid";
