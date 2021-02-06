# Introduction
This folder contains the scripts and code for the creation of a PostgreSQL server instance running in a container.
The aim is to allow a container to be spun up as needed for testing and development purposes. 
**Currently, there is no persistence of data across container instances.** That is, once a container is deleted, 
the database data housed in that container is also removed. A container however can be stopped, started 
and restarted as many time as needed without fear of losing the data. 

# How to spin up the Postgres server instance
To spin up the container running the postgre server, execute the script titled 'start_container.sh' in this folder
by running the following code:
```bash
sudo ./start_container.sh
```
**NOTE:** It should be noted that this script tears down any existing containers and spins up a new instance in its place.
**Thus, data from the last instance is deleted when this script is used to create a new instance!**

# Which port to connect to
In order to talk to the postgres server, you need to connect to the port on which the server is listening.
**This is the TCP port number 5432.**

# Going inside the container
Should the need arise, it is possible to enter the container for debugging purposes. To do so, ensure your container is up
and running first. Once it is running, note either the container name or the container id as this will be needed. This can
be seen in the output of the following command:
```bash
sudo docker ps -a
```
Once you have the id, input the following command to connect to a bash terminal instance inside the container.
```bash
sudo docker exec -it <container_name_or_id> bash
```
This should give you a terminal that you can use to explore the container. Exiting the shell returns you to your 
host machine's terminal.