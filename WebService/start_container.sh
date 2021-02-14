sudo docker rm web-1
sudo docker build -f ./Dockerfile -t web:1 ./docker_context/
sudo docker run --name web-1 -p 5000:5000 -it --network myNetwork web:1 /bin/bash
