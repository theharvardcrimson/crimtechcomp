Admin reference
===============

Local admin with @thecrimson.com sign-in is available at
http://local.thecrimson.com/admin/.

If you've made a superuser as described below, you can login via
http://local.thecrimson.com/admin/login?local to sidestep Google OAuth2.
From there, feel free to go into users and make your @thecrimson.com
address a superuser.


Creating a superuser
--------------------

.. code-block:: bash

    $ ./vagrant_manage.sh createsuperuser
