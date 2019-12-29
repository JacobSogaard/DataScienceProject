docker-compose up -d
addroute.cmd


docker exec c879aed144345f0395e464bb3623c260ae15bc5cf49361456dc63ef2d4f0e0cb mkdir -p $HOME/data
docker cp data.csv c879aed144345f0395e464bb3623c260ae15bc5cf49361456dc63ef2d4f0e0cb:$HOME/data/data.csv
docker cp data_sffd_service_calls.csv c879aed144345f0395e464bb3623c260ae15bc5cf49361456dc63ef2d4f0e0cb:$HOME/data/data_sffd_service_calls.csv

docker build . -t pysparkexallsmpleimage:latest 
docker run --rm --ip 172.200.0.240 --hostname pyspark --env-file hadoop.env --network hadoop pysparkexampleimage