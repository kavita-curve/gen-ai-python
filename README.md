## Instructions to setup this project ##

### Install python3 ###
Installing python3: `brew install python3`

This installs pip3 automatically. Any python3 package can installed as `pip3 install <package_name>`


### Installing a virtual environment ###
Run: `pip3 install virtualenv virtualenvwrapper`

Run: `mkdir .virtualenvs` in your home folder

Run: `mkvirtualenv genAI` to create a package to install libraries for the current project


### Setting up a few environment variables on macOS ###
In ~/.bashrc or ~./profile, add these:
- `export WORKON_HOME=$HOME/.virtualenvs`
- `export VIRTUALENVWRAPPER_PYTHON=/opt/homebrew/bin/python3`; path can be obtained through `which python`
- `export VIRTUALENVWRAPPER_VIRTUALENV=/opt/homebrew/bin/virtualenv`; path can be obtained through `which virtualenv`
- Load the bash file with `source ~/.bashrc` whichever you have modified

### Setting up virtualenv ###
- `source /opt/homebrew/bin/virtualenvwrapper.sh`; folder is the same as `which virtualenv`

### Install plugins ###
Run: `pip3 install -r requirements.txt`

### Enable existing virtual environment ###
Run: `source ~/.bashrc`

Run: `source /opt/homebrew/bin/virtualenvwrapper.sh`; ensure to load virtual environment

Run: `workon genAI`; current virtual environment name set above


### Running dev server ###
Run: `FLASK_APP=manage.py flask run`


### After adding a plugin ###
Run: `pip3 freeze > requirements.txt`