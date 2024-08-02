Page objects for the dimeshift application. Scripts to run test generation experiments.

### Run the application

Execute the Bash script to initialize the Docker image containing the web application:

`./run-docker.sh`

Inside the container, start the application server and MySQL:

`./run-services-docker.sh`

The application shall run at the address:

`http://localhost:3000`

### Admin Credentials
No user is pre-registered. In order to use the functionalities of the application a new user has to be registered.

### Stop application and remove container
Type `^C` in the terminal and then type `exit` to exit from the container. In order to remove the container type `docker rm $(docker ps -aq)`. The command will remove all stopped containers.
