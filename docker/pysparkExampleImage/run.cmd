docker-compose up -d
addroute.cmd

docker exec ac2a0a3aa4b0031cfeb6ea730af1e624f8c2ac5e894c74d09d712d3734f679f2 mkdir -p ./data
docker cp data.csv ac2a0a3aa4b0031cfeb6ea730af1e624f8c2ac5e894c74d09d712d3734f679f2:./data/data.csv
docker cp data_sffd_service_calls.csv ac2a0a3aa4b0031cfeb6ea730af1e624f8c2ac5e894c74d09d712d3734f679f2:./data/data_sffd_service_calls.csv

docker build . -t datascienceproject:latest 
docker run --rm --ip 172.200.0.240 --hostname pyspark --env-file hadoop.env --network hadoop pysparkexampleimage