# Project One - SimpleResponse

## About the project

SimpleResponse is a tool to make communication easier with people that sit behind their desk with headphones on.

How does it work? On a website users can log in and then they can send a message to the device that rests on the desk of the person you want to reach. Once the device receives the message, lights will flicker to alert the person. After that the person can respond with a joystick with some quick replies, replies like: “Yes”, ”No”, ”Okay”, ”I’ll be there”.

In the device there also is a temperature sensor and a light sensor. The temperature, the light intensity and the time can be seen on the LCD display.
On the website you are able to see the values of the sensors but you can also control a fan and LEDs. For the fan you can set the temperature that you would like. If it's hotter than the temperature you want, the fan will turn on. You can put the LEDs on and off or you can put it on automatic mode. With automatic mode the LEDs will turn on when it's dark.

On the website you are also able to see the history of some data. You can see the amount of messages that are sent per day and you can check the temperature the last 24 hours, week or all time.

## Getting started

### Steps

- Connecting Visual Studio Code with SSH to the Raspberry Pi
- Cloning the repository to Visual Studio Code
- Setting up the database
- Change some of the settings of the Pi
- Changing settings for front-end

### Connecting Visual Studio Code to Raspberry Pi

In order to connect Visual Studio Code to your Raspberry Pi you need to know the IP address of your Pi. After that you need to change your ethernet port settings in windows and make sure you are in range of your Pi. In my case the IP address of the Pi was **192.168.168.169** so i changed my port settings to a static IP address: **192.168.168.170**

Now that you are able to find your Raspberry Pi, you need to open Visual Studio Code go to extensions, and download Remote SSH.
When it's installed you can click on the green icon on the bottom left corner. There you will need to fill in the IP address of your Raspberry Pi and you will need to enter the password of your Pi.

### Cloning the Repository

In my github you press the green Code button and there you copy the url and paste it in your Visual Studio Code.

### Setting up the database

First you need to install/open MySQLWorkbench, once opened you need to make a new connection. Follow these steps:

- **Connection Method:** Standard TCP/Ip over SSH
- **SSH Hostname:** The ip of your Raspberry Pi, in my case 192.168.168.169
- **SSH Username:** The username of your Raspberry Pi
- **SSH Password:** The password of your Raspberry Pi
- **MySQL Hostname:** 127.0.0.1
- **MySQL Server Port:** 3306
- **Username:** The username of your Raspberry Pi
- **Password:** The password of your Raspberry Pi

Then connect to your SSH database, open the MySQL dump file in MySQL workbench and run it. Now you've created the database.

### Change some of the settings of the pi

Once you connected Visual Studio Code to your pi, follow these steps:

1. Type in your terminal
   ```sh
   sudo raspi-config
   ```
2. Open Interface Settings and enable One-Wire, I2C and SPI
3. Reboot the Raspberry Pi

### Making the back-end run automatically

1. Make a file with the name _simpleresponse.service_
2. Put the following code inside of the file:
   ```sh
   [Unit]
   Description=ProjectOne Project
   After=network.target
   [Service]
   ExecStart=/usr/bin/python3 -u /home/student/<name_of_the_repo>/backend/app.py
   WorkingDirectory=/home/student/<name_of_the_repo>/backend
   StandardOutput=inherit
   StandardError=inherit
   Restart=always
   User=student
   [Install]
   WantedBy=multi-user.target
   ```
3. Copy this file to /etc/systemd/system with this command:
   ```sh
    sudo cp simpleresponse.service /etc/systemd/system/simpleresponse.service
   ```
4. Enable the service
   ```sh
   sudosystemctl enable simpleresponse.service
   ```

### Changing settings for front-end

In order to see the correct front-end you need to follow these steps:

1. Type in your terminal
   ```sh
   sudo -i
   ```
2. Then
   ```sh
   nano /etc/apache2/sites-available/000-default.conf
   ```
3. Change DocumentRoot /var/www/html to DocumentRoot/home/student/<name_of_the_repo>/front-end
4. Save the document: Ctrl + x then Y and enter
5. Then type
   ```sh
   service apache2 restart
   ```
6. Type
   ```sh
   nano/etc/apache2/apache2.conf
   ```
7. Change
   ```sh
   <Directory />
   Options FollowSymLinks
   AllowOverride All
   Require all denied
   </Directory>
   ```
   To this:
   ```sh
   <Directory />
    Options Indexes FollowSymLinks Includes ExecCGI
    AllowOverride All
    Require all granted
    </Directory>
   ```
8. Save the file
9. Restart
   ```sh
   service apache2 restart
   ```

- Wat is de structuur van het project?
- Wat moet er gebeuren met de database? Hoe krijgt de persoon dit up and running?
- Moeten er settings worden veranderd in de backend code voor de database?
- Runt de back- en front-end code direct? Of moeten er nog commando's worden ingegeven?
- Zijn er poorten die extra aandacht vereisen in de back- en/of front-end code?

## Instructables

For more details make sure to check out my instructables: https://www.instructables.com/preview/E6RU81QL2ATLD47/
