Setup on Mac
===============


Setting up the Crimson Code in your local computer is very easy

Required Softwares
-----------------

The following softwares required before you get started:

-  VirtualBox (https://www.virtualbox.org/)
-  Vagrant (http://www.vagrantup.com/)
-  Vagrant vagrant-vbguest plugin
   (https://github.com/dotless-de/vagrant-vbguest)
-  Python 2 (*not* Python 3)
-  virtualenv (``pip install virtualenv``)
-  virtualenvwrapper (``pip install virtualenvwrapper``)


You need to append a few lines to .bashrc_profile in the root::

	 export WORKON_HOME=$HOME/.virtualenvs
	 source /usr/bin/virtualenvwrapper.sh

Try running this script with::

	 $ bash .bashrc_profile

If it doesn't run or returns errors, try changing **/usr/bin** with **/usr/local/bin**. If it still doesn't work, then you might be running a different pip. Try reinstalling virtualenv with pip2.7::

	 $ pip uninstall virtualenv virtualenvwrapper
	 $ pip2.7 install virtualenv virtualenvwrapper


Once you get the **.bash_profile** working, create a new Virtual Environment::

	 $ mkvirtualenv crimson

Inside the virtual Environment, git clone the crimson repository.::

	 $ git clone https://github.com/harvard-crimson/crimsononline


Inside **crimsononline/crimsononline/** copy **sample_local_settings.py** to **local_settings.py**::

	 $ cp sample_local_settings.py local_settings.py

You are good to go now. Fire up the Vagrant machine and run setup::

	$ vagrant up
	$ fab vagrant setup

If it runs without error, you are done. Go to local.thecrimson.com in your browser/
