CREATE TABLE "Warehouse".condensed_stock_prices
(
	dateid INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	date date NOT NULL,
	disney_volume numeric,
	disney_open numeric,
	disney_closed numeric,
	disney_high numeric,
	disney_low numeric,
	sp_500 numeric,
	dow_jones numeric
)


INSERT INTO  "Warehouse".condensed_stock_prices
(
	date,
	disney_volume,
	disney_open,
	disney_closed,
	disney_high,
	disney_low,
	sp_500,
	dow_jones
)
SELECT	
	sp1.date,
	sp1.volume AS 		disney_volume,
    sp1.open   AS 		disney_open,
    sp1.closed AS 		disney_closed,
    sp1.high   AS 		disney_high,
    sp1.low    AS 		disney_low,
    sp2.volume AS 		sp_500,
    sp3.volume AS 		dow_jones
FROM "Warehouse".stock_price AS sp1
INNER JOIN "Warehouse".stock_price AS sp2
ON
	sp1.date = sp2.date AND sp2.stock_name = 'SP500'
INNER JOIN "Warehouse".stock_price AS sp3
ON
	sp1.date = sp3.date AND sp3.stock_name = 'Dow Jones'
WHERE
	sp1.stock_name = 'Disney'





