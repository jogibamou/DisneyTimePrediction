CREATE TABLE  "Warehouse".stock_price_buffer
(
	stock_name varchar(16),
	date date NOT NULL,
	volume decimal,
	open decimal,
	high decimal,
	low decimal
)