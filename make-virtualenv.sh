#! /bin/bash

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
VIRTUALENV_DIR=$SCRIPT_DIR/jingle-env

if [ ! -d $VIRTUALENV_DIR ]
then
    echo Making virtual environment in $VIRTUALENV_DIR
    virtualenv -p /usr/bin/python3 $VIRTUALENV_DIR
fi

echo Setting up virtualenv
$VIRTUALENV_DIR/bin/pip install -r requirements.txt

echo Installing local identijingle to virtualenv
$VIRTUALENV_DIR/bin/easy_install $SCRIPT_DIR

rm -rf $SCRIPT_DIR/build
rm -rf $SCRIPT_DIR/temp
rm -rf $SCRIPT_DIR/*.egg-info
