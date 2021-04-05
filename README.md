# Day-Trading-System-Seng468
This is a distributed day trading system created as part of the course project for SENG 468 at the University of Victoria, Spring 2021.
It is comprised of numerous independent services that together form the entire system. To start the system it is assumed that docker is installed and the user is able to execute the provided shell scripts.

# How to Start the System
The system's various services need to be started in a certain order for successful start-up. This method will change slightly depending on if you run on the lab VM provided for the course or on a personal device.

## Starting on Lab VM
1. Cloning the project and navigate to the root directory. 
2. Execute the shell script `start_service.sh` to spin up the independent services in the system. 
3. Ensure that the services are running by executing the command `sudo docker ps -a` in the terminal and looking for the following docker images:
* web-1
* cache-1
* trigger-1
* audit-1
* dbmgr-1
* trading-db-13
* redis-1
* mongo-db-4.4

## Starting on Local Machine
1. Cloning the project and navigate to the root directory. 
2. Open the `config.py` file and navigate to the bottom.
3. Change `LEGACY_STOCK_SERVER_IP = '192.168.4.2'` to be `LEGACY_STOCK_SERVER_IP = 'dummy-stock-1'` and save the file.
4. Execute the shell script `deploy_config.sh`.
5. Perform the same steps starting at step 2 in `Starting on Lab VM` seen above.

# Running the System
The following can be done to either run the system with the workload generator or the web UI client. This assumes that the previous steps defined in `How to Start the System` have been performed. 

## Running the Generator
1. Navigate to the `WorkloadGenerator` directory from the root directory.
2. To change the workload file being run, open the generator `/docker_context/MultiGenerator.py`.
3. Specify the txt workload file and the corresponding number of users i.e. `<num_users>_user_workload.txt`.
4. From within the `WorkloadGenerator` folder run the shell script `start_service.sh`.
5. From here you can run the command `python MultiGenerator.py` to start the generator.

## Running the Web UI Client
1. Navigate to the `client-user` directory from the root directory.
2. Execute the shell script `start_client.sh` to intialize the docker container and start the React app.
3. Navigate to the URL `http://localhost:3000` in your web browser.

# Troubleshooting
The following are common troubleshoots in case something is not working or if you want to analyse the system with more detail.

## Docker Images Appearing on System Start
This is commonly caused by issues with the shell scripts not being executable after cloning from Github. 
To resolve this run the commands `chmod 755 *.sh`, `chmod 755 */*.sh`, `chmod 755 */*/*.sh` and retry starting the system.

## Generator Failing to Start
This is often caused by misplacing the number of users when changing the file. Ensure the the `NUM_USERS` field matches with the number of users on the workload file.

## Running in Debug Mode
To run the system in debug mode do the following:
1. Navigate to the root directory of the project.
2. open the `config.py` file.
3. Change `RUN_DEBUG=False` to `RUN_DEBUG=True` 
4. Run the shell command `deploy_config.sh` 
5. Restart the system
Note that this will significantly slow the system down

## View Service Logs
You can view the individual serivce logs by running `docker logs <container_image_name`
