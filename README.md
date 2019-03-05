{% comment "This comment section will be deleted in the generated project" %}
# Django uWSGI template

This is a [Django](https://docs.djangoproject.com) project template using [uWSGI](https://uwsgi-docs.readthedocs.io) as application server.

> **NOTE** : for OSX check [uwsgi-emperor-mode](https://github.com/20tab/uwsgi-emperor-mode) to configure your own local server with emperor.

## Setup

We suggest updating pip to the latest version and using a virtual environment to wrap all your libraries.

### Virtual environment

Choose one of these options to create an empty virtual environment, with the right python version, and activate it:

> **NOTE** : replace `venvs` with your actual virtual environments directory and `project_name` with your actual project name.

#### Python 2

```shell
$ pip install --user -U pip virtualenv
$ virtualenv --python=python3 ~/venvs/project_name
$ source ~/venvs/project_name/bin/activate
```

#### Python 3
```shell
$ pip3 install --user -U pip
$ python3 -m venv ~/venvs/project_name
$ source ~/venvs/project_name/bin/activate
```

#### Virtualenvwrapper

Alternatively, use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/) for an easier workflow.

```shell
$ pip install --user -U pip virtualenvwrapper
$ mkvirtualenv --python=python3 project_name
$ workon project_name
```

### Basic requirements

Django and Invoke must be installed before initializing the project.

```shell
(project_name) $ pip install -U django invoke
```

### Start Project

Change directory and start a new project with this template:

> **NOTE** : replace `projects` with your actual projects directory.

```shell
(project_name) $ cd ~/projects/
(project_name) $ django-admin.py startproject --template https://www.20tab.com/template/ -e cfg,ini,md,py,yaml,template -n Makefile project_name
```

### Git initialization

In order to initialize git and sync the project with an existing repository:

> **NOTE** : replace `git_repository_url` with your actual git repository url.

```shell
(project_name) $ cd ~/projects/project_name
(project_name) $ inv gitinit git_repository_url
```

Rest of this README will be copied to the generated project.

--------------------------------------------------------------------------------------------

{% endcomment %}# {{project_name}}

This is a [Django](https://docs.djangoproject.com/en/{{docs_version}}/) project using [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) as application server.

> **NOTE** : for OSX check [uwsgi-emperor-mode](https://github.com/20tab/uwsgi-emperor-mode) to configure your own local server in emperor mode.

## Setup

We suggest updating pip to the latest version and using a virtual environment to wrap all your libraries.

### Virtual environment

Choose one of these options to create an empty virtual environment, with the right python version, and activate it:

> **NOTE** : replace `venvs` with your actual virtual environments directory.

#### Python 2

```shell
$ pip install --user -U pip virtualenv
$ virtualenv --python=python3 ~/venvs/{{project_name}}
$ source ~/venvs/{{project_name}}/bin/activate
```

#### Python 3
```shell
$ pip3 install --user -U pip
$ python3 -m venv ~/venvs/{{project_name}}
$ source ~/venvs/{{project_name}}/bin/activate
```

#### Virtualenvwrapper

Alternatively, use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/) for an easier workflow.

```shell
$ pip install --user -U pip virtualenvwrapper
$ mkvirtualenv --python=python3 {{project_name}}
$ workon {{project_name}}
```

### Basic requirements

Django and Invoke must be installed before initializing the project.

```shell
({{project_name}}) $ pip install -U django invoke
```

### Clone Project

Change directory and clone the project repository:

> **NOTE** : replace `projects` with your actual projects directory.

```shell
({{project_name}}) $ cd ~/projects/
({{project_name}}) $ git clone git_repository_url {{project_name}}
```

> **NOTE** : If you're cloning an existing project, make sure you go to the correct branch (e.g. `git checkout develop`)

### Initialization

Enter the newly created **project** directory:

```shell
({{project_name}}) $ cd ~/projects/{{project_name}}
```

Invoke init and follow instructions, to configure the project:

```shell
({{project_name}}) $ inv init
```

## Usage

### Database reset

To reset database execute (beware all data will be lost):

```shell
({{project_name}}) $ inv dropdb
({{project_name}}) $ inv createdb
({{project_name}}) $ python manage.py migrate
```

### Superuser creation

Create a user with full privileges (e.g. admin access):

```shell
({{project_name}}) $ python manage.py createsuperuser
```

### Add or Update libraries

#### List outdated libraries

To list all outdated installed libraries:

```shell
({{project_name}}) $ pip list -o
```

#### Edit and Compile requirements files

Edit the appropriate .ini requirements file, to add/remove pinned libraries or modify their versions.

To update the compiled requirements files (`requirements/*.txt`), execute:

```shell
({{project_name}}) $ make pip
```

Alternatively, in order to update specific dependent libraries to the latest version (e.g. urllib3), execute:
￼
```shell
({{project_name}}) $ make pip p='-P urllib3'
```

### Install libraries

To install the just updated requirements (e.g. `requirements/dev.txt`), execute:

```shell
({{project_name}}) $ make dev
```

## Testing

To run the full test suite (including `behave` tests), with coverage calculation, execute:

```shell
({{project_name}}) $ make test
```

> **NOTE** :  check [django-bdd-toolkit](https://github.com/20tab/django-bdd-toolkit) for instructions on how to write BDD tests

## Frontend build

In order to install `node` dependencies and compile the frontend code, execute:

```shell
({{project_name}}) $ make npm
```

## Continuous Integration

Use the following command as a shortcut to configure a continuous integration (e.g. Jenkins) build:

```shell
make ci PASSWORD=<db_user_password> SECRETKEY=<django_secret_key>
```

## Deploy

The project is partially configured to use Ansible to deploy the project. For each instance to deploy (e.g. "alpha"), there must be a config file (e.g. `deploy/alpha.yaml`) and an item in the hosts file .

Use provided `deploy/alpha.yaml.template` and `deploy/hosts.template` as templates for, respectively, the configuration and the hosts files. Rename them removing the `.template` suffix. The obtained files will not be versioned.

This project contains makefile commands for "alpha". If needed, duplicate those and use them as templates for additional instances (e.g. "beta" or "prod").

Both the remote server and the continuous integration system need `node.js`, in order to automatically build static files. If such module bundler is not necessary, remove unused commands from the Makefile `ci` command and from `deploy/deploy.yaml`.

Each instance (e.g. "alpha") should be initialized, executing only **once**:

```shell
({{project_name}}) $ make initalpha
```

To deploy a specific instance (e.g. "alpha"), execute:

```shell
({{project_name}}) $ make alpha
```
