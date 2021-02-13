sudo docker rm audit-1
sudo docker build -f ./Dockerfile -t audit:1 ./docker_context/
sudo docker run --name audit-1 -p 6500:6500 -it --network myNetwork audit:1 /bin/bash
