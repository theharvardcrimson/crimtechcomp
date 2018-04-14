Setup on Windows
================

Foreward
--------

You may be able to get everything set up by installing Cygwin (make sure
to install ssh, python, and git), and then following the Unix
instructions.


Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

-  VirtualBox (https://www.virtualbox.org/)
-  Vagrant (http://www.vagrantup.com/)
-  Python

Make sure that python is in your PATH environment variable.

Install pip, virtualenv, virtualenvwrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(The following instructions are based on
http://www.tylerbutler.com/2012/05/how-to-install-python-pip-and-virtualenv-on-windows-with-powershell/)

1. Download the pip installer
   https://raw.github.com/pypa/pip/master/contrib/get-pip.py

2. Open a PowerShell window at that location

3. Run the installer::

    python get-pip.py

4. Add the path to ``pip`` to you PATH environment variable (this will
   likely be ``<python dir>/Scripts``)

5. Close and reopen PowerShell to refresh its path

6. Install virtualenv::

    pip install virtualenv

7. Install virtualenv-wrapper::

    pip install virtualenvwrapper-powershell

8.  Open a new PowerShell window **with administrator privileges**

9.  Allow importing modules: ``Set-ExecutionPolicy Unrestricted``

10. Make a directory for virtualenvs ``mkdir '~\.virtualenvs'``

11. Import the wrapper module::

    Import-Module virtualenvwrapper


You can safely ignore ``Get-Content : Cannot find path 'Function:\TabExpansion' because it does not exist.``

12. Create a virtual env (assuming you are calling it "crimson")::

    mkvirtualenv crimson

Install developer requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install MVC for Python (this plus the next two allow pip to compile
   packages on Windows)

   http://aka.ms/vcpython27

2. Install MSVC Redist 2008 (x86)

   http://www.microsoft.com/en-us/download/details.aspx?id=29

3. Install MSVC Redist 2008 (64-bit)

   http://www.microsoft.com/en-us/download/details.aspx?id=15336

4. Manually download and install pycrypto 2.1 (pip has issues installing
   this)

   http://www.voidspace.org.uk/downloads/pycrypto-2.1.0.win32-py2.7.zip

5. Install deveoper requirements

``pip install -r developer-requirements.txt``

If you have issues with the above steps, try the following (taken from
http://springflex.blogspot.com/2014/02/how-to-fix-valueerror-when-trying-to.html)
and redo the instructions in the previous section

1. Install Microsoft Visual Studio 2008 Express Edition. The main Visual
   Studio 2008 Express installer is available from

   https://www.dreamspark.com/Product/Product.aspx?productid=34

   This package can be installed using the default options.

2. Install the Microsoft Windows SDK.

http://www.microsoft.com/downloads/details.aspx?FamilyId=F26B1AA4-741A-433A-9BE5-FA919850BDBF&displaylang=en

Download the Windows Server 2008 & .NET 3.5 SDK. Do not install beta or
'Release Candidate' (RC) versions. Also do NOT install "Microsoft
Windows SDK for Windows 7 and .NET Framework 4" (version 7.1); if you
want to use a 7.x version choose the "Microsoft Windows SDK for Windows
7 and .NET Framework 3.5 SP1".

::

     While installing the SDK, you must select "x64 Compilers and Tools". For example, in the SDK installer above:

On the screen "Installation Options" Select "Developer Tools"->"Visual
C++ Compilers". This item has the Feature Description "Install the
Visual C++ 9.0 Compilers. These compilers allow you to target x86, x64,
IA64 processor architectures."

3. To verify that you have all installed components, check that the
   Microsoft SDK contains the "amd64" version of the C/C++ compiler
   "cl.exe". This is usually installed into
   ``C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\amd64\cl.exe``

4. copy ``.../VC/bin/vcvars64.bat`` to ``.../VC/bin/vcvarsamd64.bat``

5. copy ``.../VC/bin/vcvars64.bat`` to
   ``.../VC/bin/amd64/vcvarsamd64.bat``

Bootstrapping a local VM
------------------------

1. Run ``vagrant plugin install vagrant-vbguest``

May have to edit system PATH environment variable to use legacy folder
names like ``PROGRA~1`` or if you installed vagrant in a path whose name
has spaces

2. Run ``vagrant up`` to bring up a VirtualBox VM running Ubuntu 12.04
   and to provision it with most of the requirements needed to run our
   webserver. This command downloads an Ubuntu image, builds a VM, and
   then runs the script ``bootstrap_vagrant.sh``, which you can look at
   to better understand what our server is composed of.

3. Copy over ``sample_local_settings.py`` as ``local_settings.py`` and
   enter your AWS API keys into the new ``local_settings.py`` file:

   ::

       AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
       AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

4. Run setup Fabric task on your host machine (not in the VM -- make
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

You may have to specify the full path of fab in your virtualenv, or add
that path to you PATH environment variable. The full path will look like
``C:\User\<name>\.virtualenvs\crimson\Scripts\fab.exe``

5. Finally, point your browser to http://localhost:8080/ to access the
   web app and develop away! Getting Started

Download & Install Virtualbox

Download & Vagrant from https://www.vagrantup.com/downloads.html Run
installer May have to clear C:<user>or reset its permissions

via
http://www.tylerbutler.com/2012/05/how-to-install-python-pip-and-virtualenv-on-windows-with-powershell/
Install Python Download pip installer
https://raw.github.com/pypa/pip/master/contrib/get-pip.py Run installer
May have to add pip to environment variables Add python to PATH Restart
console Run pip install virtualenv Run pip install
virtualenvwrapper-powershell Restart PowerShell as administrator
Set-ExecutionPolicy Unrestricted mkdir '~.virtualenvs' Import-Module
virtualenvwrapper You can safely ignore “Get-Content : Cannot find path
'Function:' because it does not exist.”

mkvirtualenv crimson

The following are needed so that pip can compile packages on Windows
Install MVC for Python: http://aka.ms/vcpython27 Install MSVC Redist
2008 (x86) http://www.microsoft.com/en-us/download/details.aspx?id=29
Install MSVC Redist 2008 (64-bit)
http://www.microsoft.com/en-us/download/details.aspx?id=15336 Manually
download and install pycrypto 2.1 (pip has issues installing this)
http://www.voidspace.org.uk/downloads/pycrypto-2.1.0.win32-py2.7.zip pip
install -r developer-requirements.txt If you have issues, try the
following steps
(http://springflex.blogspot.com/2014/02/how-to-fix-valueerror-when-trying-to.html)
1. Install Microsoft Visual Studio 2008 Express Edition. The main Visual
Studio 2008 Express installer is available from (the C++ installer name
is vcsetup.exe):
https://www.dreamspark.com/Product/Product.aspx?productid=34 This
package can be installed using the default options. 2. Install the
Microsoft Windows SDK. The Microsoft Windows SDK is available by
searching Microsoft's download site, or by going directly to:
http://www.microsoft.com/downloads/details.aspx?FamilyId=F26B1AA4-741A-433A-9BE5-FA919850BDBF&displaylang=en
Download the Windows Server 2008 & .NET 3.5 SDK. Do not install beta or
'Release Candidate' (RC) versions. Also do NOT install "Microsoft
Windows SDK for Windows 7 and .NET Framework 4" (version 7.1); if you
want to use a 7.x version choose the "Microsoft Windows SDK for Windows
7 and .NET Framework 3.5 SP1". 2.1. While installing the SDK, you must
select "x64 Compilers and Tools". For example, in the SDK installer
above: On the screen "Installation Options" Select "Developer
Tools"->"Visual C++ Compilers". This item has the Feature Description
"Install the Visual C++ 9.0 Compilers. These compilers allow you to
target x86, x64, IA64 processor architectures." 3. To verify that you
have all installed components, check that the Microsoft SDK contains the
"amd64" version of the C/C++ compiler "cl.exe". This is usually
installed into C:Files (x86)Visual Studio 9.064.exe 4. copy
.../VC/bin/vcvars64.bat to .../VC/bin/vcvarsamd64.bat 5. copy
.../VC/bin/vcvars64.bat to .../VC/bin/amd64/vcvarsamd64.bat

vagrant plugin install vagrant-vbguest May have to edit system PATH
environment variable to use legacy folder names like PROGRA~1 if you
installed vagrant in a path whose name has spaces

(crimson)$ fab vagrant setup You may have to specify the full path of
fab in your virtualenv, or and that path to you PATH environment
variable. Full path will look like C:<name>.virtualenvs.exe

If provisioning or setup fails, make sure you’re saving your VM to an
NTFS formatted filesystem. FAT32 has a max file size of 4GB, so you VM
disk may run out of space
