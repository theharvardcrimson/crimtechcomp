#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

export DEBIAN_FRONTEND=noninteractive

echo ">>> UPDATING VM SOFTWARE..."
echo
apt-get update -y && apt-get dist-upgrade -y && apt-get --purge autoremove -y
echo

echo
echo ">>> INSTALLING DEVELOPMENT TOOLS..."
echo
apt-get install -y python-pip git python-dev
pip install -U pip virtualenv
apt-get install -y fabric
apt-get install -y libjpeg8 libjpeg-dev zlib1g zlib1g-dev
apt-get install -y libxml2-dev libxslt1-dev
apt-get install -y nodejs nodejs-legacy npm
npm list -g bower || npm -g install bower
echo

echo
echo ">>> INSTALLING MYSQL..."
echo
apt-get install -y mysql-server-5.6 mysql-client-5.6 mysql-client-core-5.6 libmysqlclient18 libmysqlclient-dev

if ! [[ -f "nightly.sql.gz" ]]
then
  echo "Downloading db dump (this may take a few minutes)..."
  wget --progress=dot:giga --http-user=crimson --http-password=Plympton http://dbdump.thecrimson.com/nightly.sql.gz
fi

if ! mysql -uroot crimson -e "USE crimson;" &> /dev/null
then
  echo "Importing db dump (this may take a few minutes)..."
  mysql -uroot <<< "DROP DATABASE IF EXISTS crimson; CREATE DATABASE crimson DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
  mysql -uroot <<< "GRANT ALL PRIVILEGES ON crimson.* to 'crimson'@'localhost' IDENTIFIED BY 'crimson';"
  zcat nightly.sql.gz | mysql -uroot crimson || { mysql -uroot "DROP DATABASE IF EXISTS crimson;"; exit 1; }
fi

echo
echo ">>> INSTALLING MORE DEVELOPMENT TOOLS..."
echo
apt-get install -y memcached libmemcached10 libmemcached-dev
mkdir -p /srv/crimson && chown vagrant:www-data /srv/crimson
mkdir -p /srv/crimson/geoip
pushd /srv/crimson/geoip
[[ -f GeoIP.dat ]] || wget --progress=dot:mega -O - http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz | gunzip > GeoIP.dat
[[ -f GeoLiteCity.dat ]] || wget --progress=dot:mega -O - http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz | gunzip > GeoLiteCity.dat
popd

echo
echo ">>> INSTALLING APACHE..."
echo
apt-get install -y apache2 libapache2-mod-wsgi

# copy over virtualhost
cp /vagrant/server/0002-crimson-vagrant.conf /etc/apache2/sites-available/0002-crimson-vagrant.conf

# copy over supervisord confs
cp /vagrant/server/vagrant-supervisord.conf /etc/supervisord.conf
cp /vagrant/server/supervisor.init /etc/init.d/supervisor.init
update-rc.d supervisor.init defaults
update-rc.d supervisor.init enable

# Enable the new virtual host
a2dissite 000-default
a2ensite 0002-crimson-vagrant

# No one ever remembers to run `fab vagrant setup` (TODO: why should they have
# to?), so remind them with the default Apache site.
echo 'You need to run <code>fab vagrant setup</code>.' > /var/www/html/index.html

if [[ -e /srv/crimson/setup_complete ]]
then
  service apache2 restart
  echo ">>> COMPLETED PROVISIONING!"
else
  echo ">>> PLEASE RUN \`fab vagrant setup\` TO COMPLETE PROVISIONING!" >&2
fi
