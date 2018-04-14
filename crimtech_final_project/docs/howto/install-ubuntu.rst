Installing Ubuntu from Windows
==============================

crimsononline is notoriously difficult to setup, and its even more so to attempt it on Windows. A nice way to make the process easier, particularly for Windows users, is to install another operating system called Ubuntu: a free, open source, Linux operating system that has several features that make software development much easier. This tutorial will guide you through the process of installing Ubuntu *alongside* Windows (so that you can simultaneously have both Windows and Ubuntu on your computer without losing any of your Windows files). Since Ubuntu is a Unix-like operating system, take a look at the :ref:`unix_setup` instructions after installation.

 \

**Note: This tutorial will assume that you have Windows 8+. If you don't, a lot of the instructions may still be applicable, but you might have to do some independent research about installing Ubuntu on older versions of Windows. Additionally, the simplest way to install Ubuntu requires having a removable USB drive with at least 2 GB of free space. This tutorial will proceed with the assumption that you have one. If you don't have one and would like to borrow one, or if you just need help with the installation process, feel free to contact Nenya Edjah (nenya.edjah@thecrimson.com) any time.**


Instructions
------------
If you already have a bootable USB stick for Ubuntu, then skip to step 3.

1. Download Ubuntu 16.04.2 LTS from the Ubuntu website. https://www.ubuntu.com/download/desktop

2. Follow the instructions on this website, but stop after step 5. https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-windows

3. Turn off fast startup (the link says Windows 10, but it works for Windows 8 as well): https://in.answers.acer.com/app/answers/detail/a_id/37059/~/windows-10%3A-enable-or-disable-fast-startup

4. Turn off secure boot: https://www.howtogeek.com/175641/how-to-boot-and-install-linux-on-a-uefi-pc-with-secure-boot/

5. Now, Shift+Click restart as demonstrated in the previous link to go back to the boot options menu. Click ``Use a device``. Your computer should restart and show you a few options. Select the one the corresponds to your USB drive and continue.

6. You should now be taken to the Ubuntu boot menu. Select ``Install Ubuntu``.

7. Now, follow the steps in this video starting from 2:05: https://youtu.be/nBD4KqH5CT8?t=2m5s. There are, however, a couple of things to do differently/things to place emphasis on.

    * At some point, you will probably be given the option to connect to a WiFi network. Make sure you do that.

    * Make sure that ``Download updates while installating Ubuntu`` is checked.
    * Make sure that ``Install third-party software...`` is checked.
    * You will likely be presented with another option: ``Turn off secure boot``. Make sure that this is checked as well. Checking this box will require that you input a password. Do so.
    * **Install Ubuntu alongside Windows 10**. This is crucial. When given the option to partition your drives in order to allocate drive space for Ubuntu, be cautious. You want to make sure that Windows still has enough space, and you also want to try to give Ubuntu at least 40-60 GB. If you're not presented with the drive that you want to install Ubuntu on, then click the ``Select drive`` dropdown menu and select which drive you would prefer instead.
    * When prompted with the ``Write previous changes to disk and continue?`` prompt, select continue.
    * Do not select ``Encrypt my home folder``
    * When the installation process finishes, restart. If you are presented with a black screen with a few lines of text that have something to do with ``cache``, and the screen seems to stay stuck for longer that a minute, just hold down your computer's power button until your computer shuts down. Then restart.
    * You might now be presented with steps to disable Secure Boot. Follow them.
    * Otherwise, you will be presented with GRUB. This is the Ubuntu boot manager. Select the ``Ubuntu`` option to begin Ubuntu.

8. You should be able to access all of Windows files from your Ubuntu directory. Whenever you want to switch to/from Windows and Ubuntu, just restart your computer, and select the ``Windows Boot Manager`` or the ``Ubuntu`` options accordingly.

9. Feel free do some additional research or to contact Nenya Edjah (nenya.edjah@thecrimson.com) if things don't go exactly as described.
