CREATE TABLE "Warehouse"."Times" 
(
	TimeID INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
	TimeStart TIMESTAMP NOT NULL, -- This denotes the instant that the specified period begins
	MonthOfYear INT NOT NULL CONSTRAINT maximum_months CHECK (MonthOfyear <= 12),
	WeekOfYear INT NOT NULL CONSTRAINT maximum_weeks CHECK (WeekOfYear <= 52),
	DayOfYear INT NOT NULL CONSTRAINT maximum_days CHECK (DayOfYear <= 366),
	MonthName VARCHAR(10) NOT NULL CONSTRAINT valid_months CHECK
		(
			MonthName IN 
			(
				 'January'
				,'February'
				,'March'
				,'April'
				,'May'
				,'June'
				,'July'
				,'August'
				,'September'
				,'October'
				,'November'
				,'December'
			)
		),
	DayOfWeek INT NOT NULL CONSTRAINT maximum_weekdays CHECK (DayOfWeek <= 7),
	DayOfWeekName VARCHAR(10) NOT NULL CONSTRAINT valid_weekdays CHECK
		(
			DayOfWeekName IN
			(
				 'Sunday'
				,'Monday'
				,'Tuesday'
				,'Wednesday'
				,'Thursday'
				,'Friday'
				,'Saturday'
			)
		),
	Season VARCHAR(10) NOT NULL CONSTRAINT valid_seasons CHECK
		(
			Season IN
			(
				 'Spring'
				,'Summer'
				,'Fall'
				,'Winter'
			)
		)
	
)