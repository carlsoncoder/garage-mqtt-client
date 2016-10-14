# Carlson Garage MQTT Client

This is the source code for my MQTT client used on the garage door(s)

This application is designed to run on a Raspberry Pi

You need to install two dependencies, "paho-mqtt" and "pytz"  These can be installed via PIP:

        pip install paho-mqtt
        pip install pytz

You will also need an SSL certificate, private key file, and ca-bundle file.  These should be placed in the root of the directory in a folder called "certs".  Note this is NOT included in this repo.

Lastly, you will need to create a file called "config.py" in the root of the directory.  You will need to fill in the appropriate values:

        # define the clientId
        clientId = 'client-id-1'
        
        # define connection parameters to MQTT server
        mqttHost = 'www.yourserverdomain.com'
        mqttPort = 8883
        mqttKeepAlive = 60

        # define program parameters
        # how old of a message will we still accept and process (in seconds)?
        maxMessageSkewTime = 180
        # how long does the garage take to fully open or close (in seconds)?
        garageActionTime = 20

        # define the path to the certificates
        certFilePath = 'certs/yourCertificateFileName.pem'
        keyFilePath = 'certs/yourCertificateKeyName.key'
        caBundlePath = 'certs/ca-bundle.pem'
        
        # define authentication variables for MQTT broker
        username = 'yourUserName'
        password = 'yourPassword'

After this, you'll need to setup a startup script to have this run on boot.  In the directory where you placed this file (in my case, '/home/pi/HomeAutomation'), create a file called "init-garage-monitor.sh".  Put the following text in it:

        #!/bin/sh
        cd /home/pi/HomeAutomation/garage-mqtt-client
        /usr/bin/python garage-mqtt-client.py &

Now, make it executable:

        sudo chmod +x init-garage-monitor.sh

Open up crontab as sudo:

        sudo crontab -e

Add this line at the botton:

        @reboot /home/pi/HomeAutomation/init-garage-monitor.sh &

Now, when you reboot the Pi, it should automatically start up the script and run it!

Feel free to reach out to me at Twitter via [@carlsoncoder](https://twitter.com/carlsoncoder "@carlsoncoder") with any questions, or check out [my blog.](http://www.carlsoncoder.com/ "Carlson Coder Blog")

Thanks,
Justin

License
----
All code in this repository that was created by me is considered [Beerware](http://en.wikipedia.org/wiki/Beerware "Beerware")

