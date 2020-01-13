CREATE VIEW filtered_wait_times AS
SELECT
    "AWT".dataid,
    "AWT".attractionid,
    "AWT".timestamp,
    "AWT".waittime
FROM 
    "Warehouse"."AttractionWaitTimes" AS "AWT"
INNER JOIN filtered_attractions  AS "GWT"
ON
    "AWT".attractionid = "GWT".attractionid
WHERE "AWT".waittime > -1 AND EXTRACT(HOUR from "AWT".timestamp) BETWEEN 1 AND 6

ORDER BY random()

