docker build . -t flume:latest 

docker run --rm -it --ip 172.200.0.245 --hostname flume -p 44444:44444 --network hadoop flume:latest 