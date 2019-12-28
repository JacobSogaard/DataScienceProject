docker build . -t producerexample:latest 
docker run --rm --ip 172.200.1.239 --hostname producer --network kafkaNetwork producerexample:latest