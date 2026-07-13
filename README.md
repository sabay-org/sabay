## Local development setup

* highly recommend running linux (Ubuntu 24.04 (via VM if you run another host OS))
* install / setup [pyenv](https://github.com/pyenv/pyenv)
* from top-level repo directory...
* install version specified in `.python-version` file
  - `pyenv install`
* ensure you're picking up correct version of python
  - `cat .python-version && python --version`
* create virtual environment for localized package installation
  - `python -m venv .venv`
* active virtual env
  - linux / macOS: `source .venv/bin/activate`
  - windows: mmm, you should look it up; depends on terminal environment used
* install [pipenv](https://pipenv.pypa.io/en/latest/installation.html)
  - `pip install pipenv`
* install project packages
  - `pipenv install`
