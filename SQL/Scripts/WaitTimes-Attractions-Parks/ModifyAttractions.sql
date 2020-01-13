CREATE OR REPLACE FUNCTION modify_attraction(ride_name varchar(60), outdoor_ bool, speed_ SMALLINT, music_ SMALLINT, dark_ SMALLINT, 
											water_ SMALLINT, coaster_ bool, car_ bool, train_ bool, spinner_ bool, isshow_ bool, story_ bool, 
											game_ bool, simulation_ bool) RETURNS int AS $$
											BEGIN
											UPDATE "Warehouse"."Attractions" as attractions
											SET 
												outdoor = outdoor_,
												speed = speed_,
												music = music_,
												dark = dark_,
												water = water_,
												coaster = coaster_,
												car = car_,
												train = train_,
												spinner = spinner_,
												isshow = isshow_,
												story = story_,
												game = game_,
												simulation = simulation_
											WHERE ride_name = "attractions"."name";
											RETURN 0;
											END;
											$$ LANGUAGE plpgsql;