# tio-worksheet-config

Configure Tenable.io from excel worksheet data

This is alpha code and currently not supported, and subject to change. Not tested on Windows 

## Quick Install on Linux, OSX
```
You can install the CLI on OS/X or Unix with the following commands:

$ mkdir tio-worksheet-config
$ cd tio-worksheet-config
$ curl -s https://raw.githubusercontent.com/agroome/tio-worksheet-config/main/install.sh | bash

This will create a virtual environment and install the package in the created folder.

You must activate the virtual environment before running the commands.

$ source ./venv/bin/activate
(venv)$ tio-config —help
```

## Install on Unix

Create install directory
```
$ mkdir tio-worksheet-config
```

Setup virtual environment in install directory 
```
$ cd tio-worksheet-config
$ python3 -m venv ./venv
$ source ./venv/bin/activate
(venv)$ pip install --update pip
(venv)$ pip install git+https://github.com/agroome/tio-worksheet-config
(venv)$
```

## Run tio-config
The virtual environment must be activated in the sheel to run tio-config.


Install keys before running the first time.

```
(venv)$ tio-config keys
```

View help
```
(venv)$ tio-config --help
```


