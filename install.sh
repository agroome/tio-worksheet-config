#!/bin/sh

# install virtual environment
echo "#"
echo "#  INSTALLING VIRTUAL ENVIRONMENT ./venv"
echo "#"
python3 -m venv ./venv

# upgrade venv pip to latest version
./venv/bin/pip install -U pip

echo "#"
echo "#  installing tio-config "
echo "#"
echo "#    from: 'http://github.com/agroome/tio-worksheet-config'"
echo "#      to: virtual environment {$PWD}"
echo "#"
echo "#"
echo "#"
./venv/bin/pip install 'git+http://github.com/agroome/tio-worksheet-config.git'
echo 
echo "#"
echo "#  downloading sample data"
echo "#"

curl -O https://github.com/agroome/tio-worksheet-config/blob/main/tio-config.xlsx
chmod 644 ./tio-config.xlsx

echo "#"
echo "#  TO RUN: Activate virutal environment before running:"
echo "#"
echo "#     $ source ./venv/bin/activate"
echo "#"
echo "#     (venv)$ "
echo "#"
echo "#  FIRST USE: run this to configure API keys :"
echo "#"
echo "#     (venv)$ tio-config keys"
echo "#"
echo "#  FOR MAIN HELP:"
echo "#"
echo "#     (venv)$ tio-config --help"
echo "#"
echo "#  FOR COMMAND HELP:"
echo "#"
echo "#     (venv)$ tio-config <command> --help"
echo "#"

