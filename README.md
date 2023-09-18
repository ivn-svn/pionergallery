# pioner-gallery



## Getting started

To make it easy for you to get started with this template I have created a Docker installation guide. 
Docker was the technology I used to streamline my deployment process.

## Guide

# Running a Django Project: pioner-gallery

## Docker Compose Configuration

Create a `docker-compose.yml` file with the following content:

```
version: '3'
networks:
  my_network:
    driver: bridge
services:
  mysql_server:
    image: mysql:latest
    container_name: mysql_server
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root_pass
      MYSQL_DATABASE: yamadasan$mysqlanywhere
      MYSQL_USER: yamadasan
      MYSQL_PASSWORD: somepass
    ports:
      - "3306:3306"
    networks:
      - my_network
  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: phpmyadmin
    restart: always
    links:
      - mysql_server:db
    ports:
      - "9090:80"
    networks:
      - my_network
```


Run the following command to start the services:

#### bash


```
docker-compose up -d
```

## Running the Django Project

Execute these commands to run the project:

#### bash
``` 
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 9005
```


## Resolving the "Unknown Database" Error

If you encounter the "Unknown database 'yamadasan$mysqlanywhere'" error, follow these steps:

1. Log in to the MySQL container:

#### bash
    ```
   docker exec -it mysql_server mysql -u root -p
   ```

2. Create the 'yamadasan$mysqlanywhere' database:

#### sql

   ``` 
   CREATE DATABASE yamadasan$mysqlanywhere;
   ```

3. Check user's privileges:

#### sql

   ``` 
   SHOW GRANTS FOR 'yamadasan'@'%';
   ``` 

4. Grant necessary privileges:
   ``` 
   
#### sql
   ``` 
   
   GRANT ALL PRIVILEGES ON yamadasan$mysqlanywhere.* TO 'yamadasan'@'%';
   ``` 

5. Exit the MySQL shell:

#### bash

   ``` 
   exit;
   ``` 

### How to Check if the Database is Created

To verify the database creation:

1. Log in to the MySQL container:

#### bash

   ``` 
   docker exec -it mysql_server mysql -u root -p
   ``` 

2. List the existing databases:

#### sql

   ``` 
   SHOW DATABASES;
   ``` 

3. Look for the 'yamadasan$mysqlanywhere' database. If it appears, it means the database has been successfully created.

4. Exit the MySQL shell:
#### sql
   ``` 
   exit;
   ``` 

Now, try running your Django application again to see if the issue is resolved.



## Project status
Work in progress