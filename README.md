# Traffic Violation System | Full Stack Assignment 3

## By Jack Stiller, 25788983

This submission aims to showcase my knowledge of both frontend and backend web development for the module FullStack development. I aimed to create a prototype webpage for a hypothetical traffic system, showcasing both general user & admin access control - admins with the ability to view and manipulate users, officers and traffic offence details. 

# How to run:
With the source folder, execute the file "run_app.bat", which once followed to the end, will open a localhost link to access the designed website in practice. 

# Folder Structure

Building on Assignment two's submission contents, the folder structure within this has been altered to accomodate the frontend development practices I have used. Within the root folder, the updated .batch file, dockerfile and .dockerignore have been moved. In addition, there are two subfolders of:

- Frontend: containing the .css, .html and .js code
  - adminPortals: pages created for the administrator as per the brief
  - driverPortals: pages created for the drivers/general users

- Backend: the updated contents of the fastAPI implementation to accomodate my attempt at the higher grade boundaries within this assignment (implementation of CORS, etc.)

This structure was chosen to accomodate the small scale of the project, alongside keeping it understandable. This remains scalable due to it's simplistic nature, and if it were to be expanded upon in future the naming of files and location within folders allows for separation easily. 

## Dependencies (within *"requirements.txt"*
If these are not installed on the device, running "run_app.bat" will ensure they are part of the package through the docker container. 
```
fastapi
uvicorn
sqlalchemy
passlib[bcrypt]
python-jose[cryptography]
python-multipart
pymysql
```

# Reflections
## .Batch File Reflection

As proven in a previous assignment for this module, the .batch file worked than I expected with building an image and creating a new container, with the main issue of it (on repeat runs of the file) leading to a mass of "single-use" containers left in storage. To clarify, "single-use" as I wasn't using the Docker Desktop app. This clogged up my machine massively, and so this revised version builds a single image, a single container of a set name, gives the option to rebuild the image and runs both the backend and frontend environments all-in-one. The option to rebuild was included for myself testing, if I was to alter the fastAPI content (main.py), it may have warranted it.

## Dockerfile & .dockerignore Reflection

The Dockerfile and .dockerignore files are used to build the Docker Image and Container, outlining the specifications I required to make the project work due to technical issues with the GUI desktop app version. Dockerfile declares environment variables ("ENV" in the code") which are referenced in "database.py" for key data needed within the Workbench software. The HOST, PORT, USERNAME and PASSWORD are declared here (hard-coded) as these allowed me to access the database and have it operational. These, in a real-world, practical setting, would be edited to match the software on your own device, as the USERNAME and PASSWORD in particular may differ.

When run, it will copy the "requirements.txt" file into cached memory, housing all of the dependencies the project needs, and then runs a container based on the image it creates, configures the IP to a rarely-used port (9000 in this case), and runs Docker through the "CMD" code at the bottom.
Furthermore, this file ensures that "pip" is installed and the dependencies are inline with what has been declared within "requirements.txt".
