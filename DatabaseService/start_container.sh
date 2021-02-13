sudo docker rm dbmgr-1
sudo docker build -f ./Dockerfile -t dbmgr:1 ./docker_context/
sudo docker run --name dbmgr-1 -p 5656:5656 -it --network myNetwork  dbmgr:1 /bin/bash
