-- View: public.filtered_wait_times

-- DROP VIEW public.filtered_wait_times;

CREATE OR REPLACE VIEW public.filtered_wait_times_nonrandom AS
 SELECT "AWT".dataid,
    "AWT".attractionid,
    "AWT"."timestamp",
    "AWT".waittime
   FROM "Warehouse"."AttractionWaitTimes" "AWT"
     JOIN filtered_attractions "GWT" ON "AWT".attractionid = "GWT".attractionid
  WHERE "AWT".waittime > '-1'::integer

