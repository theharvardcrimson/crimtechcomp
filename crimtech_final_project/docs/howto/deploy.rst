Deploying AWS
=================

Log in to Amazon AWS and under S3 resources, find ``static.thecrimson.com``. In this S3 bucket, there is a file called ``userkeys.txt``. Download this file, append your public key in it and then upload it again.

For each ec2 machine (listed under ec2 resources),

1. Reboot the machine on the AWS console

2. SSH into the machine::

    $ ssh [username]@[ec2-machine-name]

3. Read the content of **.pass**. This is your current sudo password for the machine::

    $ less .pass

4. Using the sudo password in the **.pass** file. Change the sudo password to something you want. *Its convenient to have same sudo password for all machines*::

     $ passwd

5. Create a folder **.distlib**::

	$ mkdir .distlib

6. Inside .distlib, create folder **resource-cache**::

    $ mkdir .distlib/resource-cache

After having completed these steps, fire up your virtual environment::

    $ workon [venv name]

Add the AWS Key and Secret to **local-settings.py** inside **crimsononline**

Now run::

	 $ fab prod deploy
