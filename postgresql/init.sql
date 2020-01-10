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

