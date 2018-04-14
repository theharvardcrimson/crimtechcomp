## Getting Started

You should already have the following software on your system:

* Python - you __must__ use version 2.7
* virtualenv - tested on version 15.1.0 but any of the most recent versions should work
* (optional) virtualenvwrapper

Additionally, make sure you have MySQL on your system. You can get this by running
```
brew install mysql
```
or
```
sudo apt-get mysql-server
```

Now, install the following software on your system - in this order - to avoid as many problems as possible.

1. VirtualBox (https://www.virtualbox.org) - tested on version 5.1.18 but any of the most recent versions should work
2. Vagrant (http://www.vagrantup.com) - tested on version 1.9.3 but any of the most recent versions should work

After that, create a virtual environment (assuming that you are calling it "crimson"). Do __not__ create the virtual environment inside the `crimsononline` repo. You can create the virtual environment by running
```
$ mkvirtualenv crimson
```
or by doing
```
$ virtualenv crimson
$ source crimson/bin/activate
```
Ensure that your virtual environment is activated when you see
```
(crimson) $
```
as your prompt.

Now install the proper packages by running the following commands in order

1. `pip install -r requirements.txt`

2. `pip install -r developer-requirements.txt`

We're now ready to run the Harvard Crimson web app.

## Bootstrapping a local VM

1. Run `vagrant plugin install vagrant-vbguest` to install another item that we need for the VM. __Note:__ If this doesn't work, try running `brew install libxml2` and then `export NOKOGIRI_USE_SYSTEM_LIBRARIES=true` before attempting to install the plugin again.

2. Run `vagrant up` to bring up a VirtualBox VM running Ubuntu 12.04 and to provision it with most of the requirements needed to run our webserver. __This could take a while.__ This command downloads an Ubuntu image, builds a VM, and then runs the script `bootstrap_vagrant.sh`, which you can look at to better understand what our server is composed of.

3. Look in the `crimsononline` folder which contains folders like `ads`, `common`, and `content`. Inside this folder should be a file called `sample_local_settings.py`. Copy this file and rename it to `local_settings.py`. Then in `local_settings.py`, fill in your AWS API keys
    ```
    AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
    AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    ```

4. Run setup Fabric task on your host machine (not in the VM -- make sure you are in your virtualenv or fabric won't work properly):
    ```
    (crimson) $ fab vagrant setup
    ```
This uses fabric to run a procedure defined in `fabfile.py`. It will create a virtualenv (in the VM) and install Python packages defined in requirements.txt. It will also run the "deploy" task. In this context that means creating a symlink at /srv/crimson/releases/current that points to /vagrant. This way any code changes you make on your host machine will automagically show up inside the Vagrant VM via the VirtualBox filesystem mapping.

5. Finally, point your browser to local.thecrimson.com to access the web app and develop away! __Note:__ You might get something like `TypeError at /`. If this happens, just refresh the page; then it should work. Don't ask me why.

## The Development Environment on AWS

### How this all fits together

1. Elastic Load Balancer.

    This is going to share traffic between multiple web boxes. Note: it is called ```dev``` for the dev server. This cannot be changed without repurcussions (see below, #2). Production balancer will also be called something unique.


1. Route 53

   ```dev.thecrimson.com``` points to the ELB in #1.


1. EC2 Instance/AMI

    All instances are built off the dev.2014.03.02 AMI currently. Each time changes are made to configurations or servers (e.g. upgrading software) we need to bake a new AMI. So the "current AMI we are creating new instances from" is going to change over time.

    1. To spin up a new AMI hit "Launch Instance" > "My AMIs" > Select the current AMI we are working from.
    1. Choose the size you want (at least small, under 'General Purpose').
    1. Make sure to set the availability zone as us-east-1b (the same zone as all the other services)
    1. We should not need other storages
    1. Use the 'Name' tag to name the server, so everyone knows what this server ought to be
    1. Select an existing security group, and choose the public facing webserver

    Once the instance comes up it will automatically perform a code-checkout and attach itself to the proper load balancer (by name).

    The ```newserver.commands``` file is an outline of how the server was initially built, tested, etc.

1. User Accounts

    The script ```grabusers.sh``` is a small shell script that hits a URI (by default http://static.thecrimson.com/userkeys, but you can specify any). That is a file on S3. Enter any users and public-keys you want to be propogated. This is necessary because deploying from Fabric requires a user account. They will find a random password in a file in their home directory (`~/.pass`). They should change it to the same thing on each server (they can ssh directly to a box by using the public DNS address). This script is run whenever a box spins up through the `/etc/rc.local` script. It is run from `/etc/grabusers.sh`, NOT the version in the git repository. This is to limit potential security holes since the script runs as root.

1. Before Creating a New AMI

    When we need to create a new AMI (because configurations change, software upgrades, etc) first we are going to get rid of all the non-system users on the box. We want to have the above user script determine the non-system users on the box at all times

    To get rid of unwanted users run the ```/etc/delusers.sh``` file, using sudo. It will try and delete the user you logged in as, and it won't be able to. But we are ok with having one user left over.

    After this is done, simply log in to the AWS EC2 panel, select the server you are basing the AMI off, and select "Create Image" under the "Actions" menu. Note that this will cause a server reboot, so be sure there is at least one other server under the load balancer or there will be downtime.


1. Fabfile Changelog

    The vagrant instructions above contain a few new, or modified, fabric commands for getting things set up for local development.

    The dev environment on AWS also has a ```dev``` env in fabric. The hosts are looked up dynamically via the AWS API. Note: Instances are considered hosts based on being connected to the load balancer. So if an instance is removed (either manually, or because it falls over) it will not be found in this hosts check.

    We also have a ```restart_webserver``` command that performs a graceful restart of apache.

    Also useful is the ```git_checkout``` command, which allows you to switch the active branch on the server.

    You will also see an ```ec2_spinup``` method, that is always and only run from ```dev_localhost``` environment. This is where any application-related loading should take place when an instance spins up. This includes a code-checkout, to be up-to-date, and where the instance is actually attached to the ELB
