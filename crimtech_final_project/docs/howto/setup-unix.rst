.. _unix_setup:

Setup on UNIX
=============

crimsononline runs on `Django <https://djangoproject.com>`__, a web
application framework written in the `Python programming
language <http://python.org>`__. Our database engine is
`MySQL <http://mysql.com>`__.


Get set up
----------

To make our development environment as close as possible to our
production server environment, we use
`Vagrant <http://www.vagrantup.com/>`__, which manages a virtual Ubuntu
machine right on your computer. This virtual machine is virtualized by
`VirtualBox <https://www.virtualbox.org/>`__, which makes Ubuntu think
it has an entire computer to itself, when in reality it's running
virtually under your host OS. Our entire app runs on the virtual
machine, while you will edit the codebase and access the site from your
host machine. The install process is mostly the same for all host
operating systems, so the general procedure is:

1. Follow the host-specific `instructions`_ below for installing
   dependencies.
2. Clone the git repository to wherever you want to work on
   crimsononline. ``cd`` into this directory and stay here for the
   entire setup process!
3. Create a virtual env (this guide assumes you are calling it
   "crimson"), and install the developer environments into it (pycrypto is a is a necessary package that isn't found in developer-requirements.txt):

   ::

       $ mkvirtualenv crimson
       (crimson)$ pip install pycrypto==2.6.1
       (crimson)$ pip install -r developer-requirements.txt

You now should be able to run the Harvard Crimson web app. Make sure you
run all commands below from within your project folder and with your
virtualenv activated!

1. Run ``vagrant plugin install vagrant-vbguest``
   to install the 3rd item listed above.

2. Run ``vagrant up`` to bring up a VirtualBox VM running Ubuntu 12.04
   and to provision it with most of the requirements needed to run our
   webserver. This command downloads an Ubuntu image, builds a VM, and
   then runs the script ``bootstrap_vagrant.sh``, which you can look at
   to better understand what our server is composed of.

3. Copy over ``sample_local_settings.py`` as ``local_settings.py``
   (``cp crimsononline/sample_local_settings.py crimsononline/local_settings.py``)
   and enter your AWS API keys into the new ``local_settings.py`` file (**Skip the AWS API keys part if you're just
   running this locally**):

   ::

       AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
       AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

4. Before you provision the VM, you must provide it with more virtual memory in the form a swapfile. In order to do
   that, SSH into the vagrant machine with ``vagrant ssh``, and the follow the steps provided at this site:
   https://www.cyberciti.biz/faq/linux-add-a-swap-file-howto/

   **Note:** For step 1, just use ``sudo su`` or ``sudo -s``. Stop after step 5.


5. Run the setup Fabric task on your host machine (not in the VM -- make
   sure you are in your virtualenv or fabric won't work properly):

   ::

       (crimson)$ fab vagrant setup

This uses fabric to run a procedure defined in ``fabfile.py``. It will
create a virtualenv (in the VM) and install Python packages defined in
requirements.txt. It will also run the "deploy" task. In this context
that means creating a symlink at /srv/crimson/releases/current that
points to /vagrant. This way any code changes you make on your host
machine will automagically show up inside the Vagrant VM via the
VirtualBox filesystem mapping.

1. Run ``vagrant ssh -c "sudo service apache2 restart"``.

2. Finally, point your browser to ``http://local.thecrimson.com/`` to access
   the web app and develop away!

Required Software
-----------------

The following software is required before you get started:

-  VirtualBox (https://www.virtualbox.org/)
-  Vagrant (http://www.vagrantup.com/)
-  Vagrant vagrant-vbguest plugin
   (https://github.com/dotless-de/vagrant-vbguest)
-  Python 2 (*not* Python 3)
-  virtualenv
-  (optional) virtualenvwrapper

Installation for Mac OS X:
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note: These instructions have only been verified to work with OS X
10.8 (Mountain Lion).**

While many vendors provide native installers for OS X, we recommend
`Homebrew <http://brew.sh/>`__, a package manager for OS X.

1. Install `Homebrew <http://brew.sh/>`__.

-  Launch Terminal.
-  ``ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"``
-  ``brew update``
-  ``brew doctor``
-  If you see errors after running ``brew doctor``, see the Homebrew
   Troubleshooting section below.

1. Download Xcode and install the Command-Line Tools.

-  These give Homebrew access to command-line compilers like ``clang``
   and ``gcc`` (which is really just ``clang`` on Mac). (Some packages
   are compiled on your own machine!)
-  Install Xcode 4.6 from the Mac App Store.
-  Launch Xcode, accept the terms of use, and open the preferences
   window.
-  From the Downloads tab, install the Command Line Tools.
-  If you don't want the whole Xcode package, you can register as an
   Apple developer and download the standalone Command Line Tools from
   http://connect.apple.com/.

1. Install VirtualBox and Vagrant from the websites above.

Homebrew troubleshooting
^^^^^^^^^^^^^^^^^^^^^^^^

**Before anything** Run ``brew doctor``

**Your Homebrew is outdated** Run ``brew update``

**Suspicious git origin remote found.** Run ``brew update``

**Experimental support for using Xcode without the "Command Line
Tools":** Install Xcode Command Line Tools as per Step 3 above.

**No developer tools installed:** Install Xcode Command Line Tools as
per Step 3 above.

**An outdated version of Git was detected in your PATH:** Run
``brew upgrade git``

**Warning: /usr/bin occurs before /usr/local/bin:** Add
``PATH="/usr/local/bin:$PATH"`` to the end of ``~/.bash_profile``


.. _instructions:

Installation for Ubuntu:
~~~~~~~~~~~~~~~~~~~~~~~~

1. Install pip (Python package manager)::

    $ sudo apt-get install python-pip

2. Install virtualenv and virtualenvwrapper::

    $ sudo pip install virtualenv
    $ sudo pip install virtualenvwrapper

3. Add these lines to the bottom of your ``~/.bashrc`` and then restart your terminal::

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

4. In the terminal, run ``mkvirtualenv crimson`` ("crimson" being
   whatever you want to name your virtualenv)

5. Install VirtualBox and Vagrant from the websites above. Make sure that SecureBoot has been turned off if applicable. For Vagrant, download the Debian version: 32-bit or 64-bit depending on your system. Almost all computers made in past several years are 64-bit, so if you're in doubt just choose 64-bit. Whereas for VirtualBox, download the version that corresponds to your version of Ubuntu. There's a good chance that you're using Ubuntu 16.04, but to be sure, run ``lsb_release -a`` in your terminal. i386 corresponds to the 32-bit version, while AMD64 corresponds to the 64-bit version.

6. Run the following command to install some dependencies for a few of the developer requirements::

    $ sudo apt-get install build-essential libssl-dev libffi-dev python-dev

Installation for Fedora/CS50 Appliance:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install virtualenv/wrapper::

    sudo yum install python-virtualenvwrapper

2. Add these lines to the bottom of your ``~/.bashrc``::

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/bin/virtualenvwrapper.sh

3. In the terminal, run ``mkvirtualenv crimson`` ("crimson" being
   whatever you want to name your virtualenv)

4. Install VirtualBox and Vagrant from the websites above.
