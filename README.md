# What is Project Ostrich?
Project Ostrich is a Cyber Range Builder that Team Ostrich has built from scratch using the Django Framework, Dockers (along with Docker Engine API), Shell-in-a-box (within dockers), and much more. This project is part of our Final Year Project for our Diploma in Infocomm Security Management in Singapore Polytechnic. This builder is open-sourced - so feel free to fork it and make enhancements and continually build on our project. Do remember to credit us!

We hope that many will use Project Ostrich to train their students in Cyber Security for the future to come.

## In Case You Were Wondering...
Team Ostrich consists of:
- Joshua Lee (Team Leader)
- Marcus Kho (Assistant Team Leader)
- Dexter Gui
- Jonathan Au
- Wesley Chiau

# Deployment Guide
This documentation will guide administrators who would like to setup Project Ostrich on their own systems.

## Install Apache and WSGI
In the command line, install Apache and WSGI by typing:
```
sudo apt-get update
sudo apt-get -y install apache2 libapache2-mod-wsgi-py3
sudo a2enmod wsgi
```

## Configuring HTTPS/SSL For Apache
For the purposes of security, we deployed Project Ostrich with using HTTPS, with an SSL certificate. For our deployment, we will be using an already generated self-signed certificate provided by our sponsor.
However, you can still learn how to generate your own self-signed certificate through Justin Ellingwood’s tutorial, ‘How to Create a Self-Signed SSL Certificate for Apache in Ubuntu 16.04’, on DigitalOcean: https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04. 

## Installing and Configuring Ostrich Requirements
There will be some requirements needed to be installed on your Ubuntu server for Project Ostrich. Although they can be manually installed, Python’s Package Manager, pip, can install a list of requirements from a text file. The requirements.txt file is available on the project GitHub. 

###Install Python 3
However, before installing the requirements, do ensure that Python 3 is installed on your Ubuntu server, by running:
```
sudo python3 --version
```
You should get an output similar to this:
```
Python 3.5.2
```
If an error is thrown, like:
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'python' is not defined
```

Install Python3, by running:
```
sudo apt-get install python3
```

### Install pip3
Next, check if pip is installed, by running:
```
sudo pip3 --version
```
You should get an output similar to this:
```
pip 8.1.1 from /usr/lib/python3/dist-packages (python 3.5) 
If an error is thrown, like:
The program ‘pip’ is currently not installed. To run ‘pip3’ please ask your administrator to install the package ‘python3-pip’
```
Install pip3, by running:
```
sudo apt-get install python3-pip
```

### Install Django and Necessary Packages
Now that Python3 and pip are installed, we can download the requirements.txt file from the GitHub. The link to the GitHub is: https://github.com/joshualeejunyi/Ostrich.
The requirements.txt file should look something like this:
```
requests==2.9.1
django_filter==1.1.0
Django==2.0.6
tablib==0.12.1
django_filters==0.2.1
django-tinymce4-lite==1.7.2
django-adminlte2==0.3.0
```
In the terminal, navigate to the directory where the requirements.txt file is located, and run:
sudo pip3 install -r requirements.txt
The requirements will now be installed.
 
### Install MySQL Engine
We would also need to install the database engine, MySQL. We will be basing this guide on Jeremy Morris’ tutorial, ‘How to Create a Django App and Connect it to a Database’, on DigitalOcean.
Firstly, install the MySQL Database Connector by running in the terminal:
```
sudo apt-get install python3-dev
```
Next, we can install the necessary Python and MySQL development headers and libraries:
```
sudo apt-get install python3-dev libmysqlclient-dev
```
When you see the following:
```
After this operation, 11.9 MB of additional disk space will be used.
Do you want to continue? [Y/n]
Enter ‘y’ and hit ‘Enter’ to continue.
```
Next, install the mysqlclient library:
```
sudo pip3 install mysqlclient
During the installation, you should be prompted to enter the username and password. For Ostrich, we have set the username as “root” and the password as “r@nger2018”. You can enter any password that you prefer.
```
When mysqclient is successfully installed, you will see an output similar to this:
```
Collecting mysqlclient
  Downloading mysqlclient-1.3.12.tar.gz (82kB)
    100% |████████████████████████████████| 92kB 6.7MB/s
Building wheels for collected packages: mysqlclient
  Running setup.py bdist_wheel for mysqlclient ... done
  Stored in directory: /root/.cache/pip/wheels/32/50/86/c7be3383279812efb2378c7b393567569a8ab1307c75d40c5a
Successfully built mysqlclient
Installing collected packages: mysqlclient
Successfully installed mysqlclient-1.3.12
```

Finally, install the MySQL server, by entering the following command:
```
sudo apt-get install mysql-server
```
 
### Configure the Database
Now the MySQL is installed, ensure that the service is running, by entering:
sudo systemctl status mysql.service
You should see this:
```
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
   Active: active (running) since Sat 2017-12-29 11:59:33 UTC; 1min 44s ago
 Main PID: 26525 (mysqld)
   CGroup: /system.slice/mysql.service
        └─26525 /usr/sbin/mysqld

Dec 29 11:59:32 ubuntu-512mb-nyc3-create-app-and-mysql systemd[1]: Starting MySQL Community Server...
Dec 29 11:59:33 ubuntu-512mb-nyc3-create-app-and-mysql systemd[1]: Started MySQL Community Server.
```

However, the service is not started if you see this instead:
```
● mysqld.service
   Loaded: not-found (Reason: No such file or directory)
   Active: inactive (dead)
```

You can run the service by running:
```
sudo systemctl start mysql
```

Now, you can login to mysql by entering:
```
mysql -u root -p
```
The terminal will then prompt you for the password. Enter the password you have set above during the installation.

 
When you have successfully logged in, you should see the following:
```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 6
Server version: 5.7.20-0ubuntu0.16.04.1 (Ubuntu)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
```

Now, we would need to create the schema used for Ostrich. Enter:
```
CREATE SCHEMA CRB;
```

You should get a confirmation back in the terminal.
You can now quit MySQL and close the terminal.
 
### Download and Deploy Ostrich
Now that the prerequisites for Ostrich are mostly configured, we will be roughly following Tero Karvinen’s tutorial, ‘Django on Apache – with Python 3 and Apache mod-wsgi on Ubuntu 16.04’, at: http://terokarvinen.com/2017/django-on-apache-with-python-3-on-ubuntu-16-04. 
Firstly, add the project user and your own user to the project user’s group. This project user is a dedicated user for the deployment of the Django project.
In the terminal, enter:
```
sudo adduser cyberwsgi
```
You should be prompted to add a new password and the user’s details:
```
Enter new UNIX password: 
Full Name []: 
```

Enter any appropriate values and complete the creation of the user.
Next, lock the user created, in order to prevent log ins:
```
sudo usermod –lock cyberwsgi
```
We will then make the directory to host the project:
```
sudo mkdir /home/cyberwsgi/grouped
```
Then, we will configure the permissions and add our own user to the cyberwsgi’s group.
```
sudo chmod u=rwx,g=srwx,o=x /home/cyberwsgi/grouped
sudo chown -R cyberwsgi.cyberwsgi /home/cyberwsgi/
sudo find /home/cyberwsgi/grouped/ -type f -exec chmod -v ug=rw {} \;
sudo find /home/cyberwsgi/grouped/ -type d -exec chmod -v u=rwx,g=srwx {} \;
sudo adduser $(whoami) cyberwsgi
newgrp cyberwsgi
```

We can download the latest build of Ostrich into the folder /home/cyberwsgi/grouped. Before doing so, we need to make sure that git is installed on the server, by typing:
```
git --version
```

If git is installed, you should see the following:
```
git version 2.7.4
```

We will then create a folder called ‘github’ in /home/cyberwsgi to download the repository into.
```
sudo mkdir /home/cyberwsgi/github
cd /home/cyberwsgi/github
Now that we are in the GitHub folder, we can clone the repository.
sudo git clone https://github.com/joshualeejunyi/Ostrich
```

We will then copy the CRBv1 folder into /home/cyberwsgi/grouped:
```
sudo cp -r Ostrich/CRBv1 /home/cyberwsgi/grouped/
```

Next, we will go to the folder we just copied and configure the database to connect to the MySQL server that we have configured above.
```
cd /home/cyberwsgi/grouped/CRBv1
sudo nano CRBv1/settings.py
```

We will now be editing the settings file of the project. 

Firstly, in line 30, change the DEBUG = True to False. Next, add your domain to ALLOWED_HOSTS in the line next to the DEBUG setting.


Next, search for the field ‘DATABASES’, and configure the appropriate ‘USER’ and ‘PASSWORD’ that we have created when installing the MySQL Server.
 

Save the changes by pressing Ctrl+O, and exit by pressing Ctrl+X.

 
Now that we can connect to the MySQL server, we can create the database tables. In the terminal, enter:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
When successful, the terminal should display the following:
"image"

Now, we can test if everything is okay by running the development server.
```
python3 manage.py runserver
```

The system will check, and if there are no issues found, will display the following:
"image"

 
Now that everything is okay, we can edit the apache2 configuration files. Our SSL-enabled configuration can be found in /etc/apache2/sites-available/. Our configuration file name is cyber1-ssl.conf. This configuration file has already been configured to use our self-signed certification that we have mentioned earlier.
```
sudo nano /etc/apache2/sites-available/cyber1-ssl.conf
```

At the bottom of the configuration file, enter the following:
```
ServerName dmit2.bulletplus.com
WSGIDaemonProcess cyber443 user=cyberwsgi group=cyberwsgi threads=5 python-path=”/home/cyberwsgi/grouped/CRBv1”
WSGIScriptAlias / /home/cyberwsgi/grouped/CRBv1/CRBv1/wsgi.py
<Directory /home/cyberwsgi/grouped/CRBv1/CRBv1/>
	WSGIProcessGroup cyber443
	WSGIApplicationGroup %{GLOBAL}
	WSGIScriptReloading On
	Require all granted
</Directory>

Alias /static/ /home/cyberwsgi/grouped/CRBv1/static/

<Directory /home/cyberwsgi/grouped/CRBv1/static/>
	Require all granted
</Directory>
```
Modify the username and variables according to your own setup.

Save the file like before, by pressing Ctrl+O, and exit by pressing Ctrl+X.
We have finally completed the configuration of the server. Restart the apache2 server by entering into the terminal:
```
sudo service apache2 restart
```
You have now successfully deployed Ostrich to your server. You can access it by going to your domain in a browser.
 
## Configuring Docker Servers
As Project Ostrich is only in Phase 1, the feature to dynamically add Docker Servers and their ports is not implemented yet. Hence, we will be needing to modify the source code to suit our needs.
In our implementation, we have two servers that can serve Docker Containers. The first server is the dedicated Docker Server, with an internal IP address of 192.168.100.42. The ports dedicated to this server are between the range of 9051 to 9100, inclusive. After the ports have been used up, the service will be overflowed to the second server – in our case, the Web Server. The Web Server has an internal IP address of 192.168.100.43, with the ports between the range 9000 to 9050.

### The DockerKill() Class
First, we will be modifying the views.py, located in /home/cyberwsgi/grouped/CRBv1/ranges. Now, go to the DockerKill() class at line 80. You should see the following:
 
Adjust the port numbers ‘9051’ and ‘9050’ and the serverip accordingly. To add more than two servers at this stage, we will just have to add more else if statements and configure the if statements accordingly.
In lines 114 to 119, there same code can be seen. Adjust it accordingly as well.
 
 
### The checkPorts() Function
The functions checkPorts() at line 136 and 482 both checks the database for ports that are being used – both have to be reconfigured. We will be instructing the changes required for the first function at line 136.
The function takes information from the database and segregates them into two lists, one for the Web Server and the other for the Docker Server. This allows us to dynamically assign the port number and the IP address. After which, it checks the available port number and returns the first available port number. This allows for an organized system of maintaining our ports.
To add more than two servers at this stage, another list must be made, and the if else statements will need to be added on. Adjust the port numbers at lines 150 and 153 accordingly, to the appropriate server lists. Next, at line 158, enter the first port that will be used.
 
The next part of the code from lines 164 to 209 is to check the lowest available port number to be issued to the user. 
Make the changes below:
•	At line 164, change the “50” to the total ports allocated for your first server.
•	At line 166, change “9099” to the last port allocated for your first server.
•	At line 169, change “48” to the total ports allocated for your first server, minus two.
•	Do the same for lines 185 to lines 191.
 
You would have to do the same for the second checkPorts() function in the same views.py.
 
### The dockerContainerStart() Function
Next, the dockerContainerStart() functions must also be changed, these functions can be found at lines 211 and 557. Like before, we will be instructing for the first function at 221, as the process is the same for both functions.
At line 225 and 228, adjust the port numbers accordingly like before. At lines 227 and 230, the server IP addresses should also be adjusted.
 
 Next, adjust the Docker Engine API port numbers accordingly at lines 260, 270, 291, and 296.
 
The finalsiaburl at line 278 should also be changed according to your domain.
 
 
That should be all for this views.py. Next, we would have to make adjustments to the teachers/views.py. It can be located in /home/cyberwsgi/grouped/CRBv1/teachers/views.py.
The CreateImage Class
At line 41, just adjust the list of server IP addresses accordingly. The items in the list will be for looped and will create the image in each server.
 
### The AdminDockerKill() Class
At line 1255, adjust the if else statement accordingly to your setup. Also change the server variables to the IP addresses of your available servers
 

Congratulations! You have successfully deployed Project Ostrich to your system. 

