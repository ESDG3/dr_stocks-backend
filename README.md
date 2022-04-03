# Dr Stocks Backend Setup Guide
Prerequisite to run this project
1. WAMPServer
2. MySQL
3. Python
4. Docker
5. Postman

How to setup the backend services?
1. Unzip the zip file into a folder
2. Open the backend folder and navigate to the "database" folder
3. Start the WAMPServer
4. Open the "docker-compose.yml" file and change the docker id for the images to your own docker id.
![](/readme_img/docker_id.png)
4. Open all the SQL files using MySQL and execute/run all the files
5. Once done with the database, open a cmd terminal and cd to the "microservices" folder
6. After, proceed to type this command "docker-compose up -d" and hit enter to run it in the terminal. This is set up all the required services. 
7. Wait for about 30 seconds after the containers have been created to let the services start up.
![](/readme_img/docker_con.png)
8. Next, type this URL "localhost:1337" in your browser to access the KONGA portal.
9. Create an admin account and process to the services page.
![](/readme_img/kong-page.png)
10. Create all this services and routes as stated in the table:
    ![](/readme_img/Kong-Setup.png)
    ![](/readme_img/kong-services.png)
11. Next, go to the plugin tab for each service and add the Key Auth plugin for all services.

    ![](/readme_img/key-auth.png)
    
    For each Key Auth, under key names, add a key called "apikey" and hit enter and save.
12. Next, create a consumer called "customer" and under the credentials tab, create an api key with the key as this "NTaKvMth2Syfjf30m9dmKWXzANDRqbzh".
![](/readme_img/consumer_api_key.png)

13. Also, under the groups tab, add a group called "customer".
![](/readme_img/consumer_grp.png)

14. With this, you can open Postman and test the connection using this URL: 
    http://localhost:8000/api/v1/login?email=maryesther@gmail.com&password=dGVtcDE=
![](/readme_img/postman_login.png)

    

With this, you have successfully configured the backend services
