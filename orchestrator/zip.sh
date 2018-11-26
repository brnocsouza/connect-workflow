#!/bin/bash

# this is b/c pipenv stores the virtual env in a different
# directory so we need to get the path to it
PIPENV_FOLDER=$(pipenv --venv)

SITE_PACKAGES=$PIPENV_FOLDER/lib/site-packages
echo "Library Location: $SITE_PACKAGES"
DIR=$(pwd)

# Make sure pipenv is good to go
echo "Do fresh install to make sure everything is there"
# pipenv install

cd $SITE_PACKAGES
zip -r9 $DIR/package.zip *

cd $DIR
zip -g package.zip posts.py