sudo docker rm trsrvr-1
sudo docker build -f ./Dockerfile -t trsrvr:1 ./docker_context/
sudo docker run --name trsrvr-1 -p 6666:6666 -it --network myNetwork trsrvr:1 /bin/bash
