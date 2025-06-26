CREATE TABLE users (
	user_id 		SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	email 			VARCHAR(100) UNIQUE NOT NULL,
	password 		VARCHAR(30) NOT NULL,
	first_name 		VARCHAR(50) NOT NULL,
	last_name 		VARCHAR(50) NOT NULL
);

CREATE TABLE lookups (
	user_id 		SMALLINT UNSIGNED NOT NULL,
    stock_ticker 	VARCHAR(5) NOT NULL,
    time 			DATETIME NOT NULL,
    PRIMARY KEY (user_id, stock_ticker, time),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE VIEW lookups_by_user AS 
SELECT u.user_id, first_name, last_name, stock_ticker, time
FROM users u
JOIN lookups l ON u.user_id = l.user_id
ORDER BY u.user_id DESC, time;