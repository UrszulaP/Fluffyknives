CREATE TABLE users (
	UserID numeric NOT NULL,
	UserLogin VARCHAR(30) NOT NULL UNIQUE,
	UserPassword VARCHAR(30) NOT NULL,
	PRIMARY KEY (UserID)
	);

CREATE TABLE items (
	ItemID numeric NOT NULL,
	ItemName TEXT NOT NULL,
	ItemMainDescription TEXT,
	ItemPointsDescription TEXT,
	ItemImage TEXT,
	ItemPrice DECIMAL,
	PRIMARY KEY (ItemID)
	);