CREATE TABLE cities (
  name varchar(80),
  location point
);

CREATE TABLE clustercenters (
  id SERIAL PRIMARY KEY,
  coordinates float[]
);

CREATE TABLE kmeansoutput (
  category varchar(50),
  counts int,
  normalizedcount float,
  percent float,
  cluster integer REFERENCES clustercenters(id)
);

INSERT INTO cities VALUES('Copenhagen', '(-119.0, 53.0)');
INSERT INTO cities VALUES('San Francisco', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Oslo', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Barcelona', '(-119.0, 53.0)');
INSERT INTO cities VALUES('London', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Sofia', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Prague', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Berlin', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Bern', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Paris', '(-119.0, 53.0)');
INSERT INTO cities VALUES('Washington', '(-119.0, 53.0)');


