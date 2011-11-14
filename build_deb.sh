NAME=crawley-0.2.1

python setup.py sdist
cd dist
py2dsc $NAME.tar.gz
cd deb_dist/$NAME
sed -i 's/current/>=2.6/g' debian/control
dpkg-buildpackage -rfakeroot -uc -us
