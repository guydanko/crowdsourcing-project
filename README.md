NOTICE - this is a project installation guide for *Pycharm users on Windows*. 
Some adaptations might be necessary if you are using a different OS\IDE.

Project Instllation - please follow this teps:


a) Install Postgres:
  1. Download postgres sql - When asked for superuser name and password enter:
  username: postgres, password: admin (Must be similar to project's database configuration).
  2. open pgAdmin 4 (the Desktop app)
  3. Servers -> PostGres... -> Databases. then right click on it and create new db
  4. name it projectdb, in security tab click the + sign and make sure to choose postgres and all privilages then hit save

b) Clone the project and install requierments:
  1. Install python version 3.9.X
  2. Install pycharm professional
  3. clone project from the repositority using pycharm version control
    - make sure it has installed and setup virtual enviroment properly
  4. Install requierments


c) Install RabbitMQ:
  https://www.rabbitmq.com/install-windows.html#chocolatey
  Direct download, follow instructions, you will be required to install Erlang so make sure to install it.

d) Migrate db:
  1. run from terminal: python manage.py makemigrations 
  2. run from terminal: python manage.py migrate
                    ** optional** 
  (Only superusers can access the management part of the website and add videos)
  3. creation of superuser(if needed): 
	  run from terminal python manage.py createsuperuser (enter username, password and email. can be anything you like)
	  - username : admin
	  - email : admin@gmail.com
	  - pass : admin
	  hit y
    
    
e) Running the project:
  1)	Open Edit configurations
  2)	Click on the + icon 
  3)  Select the "Django Server" option, name it 'Project' and click on apply.
  ![Alt text](/Project.PNG?raw=true "Project runtime configuration")
  4)  Click on the + icon 
  5)  Select Python and copy the details (working directory should be your working directory):
  ![Alt text](/celery.PNG?raw=true "celery runtime configuration")
  6) Click on the + icon 
  7) Select Compound and add both the 'Project' configuration and the 'celery' configuration.
  ![Alt text](/django and celery.PNG?raw=true "django and celery compund runtime configuration")
  
d) use the compound configuration to run the project.
  Enjoy! :)
