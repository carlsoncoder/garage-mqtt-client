# Carlson Garage MQTT Client

This is the source code for my MQTT client used on the garage door(s)

This application is designed to run on a Raspberry Pi

You will need an SSL certificate, private key file, and ca-bundle file as well.  These should be placed in the root of the directory in a folder called "certs".  Note this is NOT included in this repo.

Lastly, you will need to create a file called "config.py" in the root of the directory.  You will need to fill in the appropriate values:

        # define the clientId
        clientId = 'client-id-1'
        
        # define connection parameters to MQTT server
        mqttHost = 'www.yourserverdomain.com'
        mqttPort = 8883
        mqttKeepAlive = 60
        
        # define the path to the certificates
        certFilePath = 'certs/yourCertificateFileName.pem'
        keyFilePath = 'certs/yourCertificateKeyName.key'
        caBundlePath = 'certs/ca-bundle.pem'
        
        # define authentication variables for MQTT broker
        username = 'yourUserName'
        password = 'yourPassword'

Feel free to reach out to me at Twitter via [@carlsoncoder](https://twitter.com/carlsoncoder "@carlsoncoder") with any questions, or check out [my blog.](http://www.carlsoncoder.com/#/blog/2014_11_06_Custom-login-authentication-with-Nancy-and-csharp "Carlson Coder Blog")

Thanks,
Justin

License
----
All code in this repository that was created by me is considered [Beerware](http://en.wikipedia.org/wiki/Beerware "Beerware")

