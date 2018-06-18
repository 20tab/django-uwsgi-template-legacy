{{project_name}}
================

This is a [Django](https://www.djangoproject.com/) template with custom configuration. It requires [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) as application server.

## Prerequisite

To use this template you need latest Django and Fabric3 version.

```
sudo pip3 install django fabric3
```

## Installation

To start a new project with this template:

```
django-admin.py startproject --template=https://github.com/20tab/twentytab_project/zipball/master -e py -e ini -e txt -e md -e yaml -e coveragerc {{project_name}}
```

## Configuration

- To configure project with virtualenv and required empty directories: 
  - check `requirements/dev.ini` to customize your virtualenv 
  - check `{{project_name}}.ini` to customize your workarea root and project root
  - and than execute `fab configure_project` into your project directory

- To merge your project with git repository execute `fab gitclone:<your_repo_git_url>`

- If you use uwsgi with emperor mode you have to create symbolic link of `{{project_name}}.ini` into vassals directory

- Check settings and urls to configure django applications

- Enjoy

## Setup

### Enviroment setup

Execute only once.

```shell
mkdir -p ~/venvs
python3.6 -m venv ~/venvs/{{project_name}}
cd ~/projects
git clone {{project_name}}@gitlab.{{project_name}}.com:{{project_name}}/{{project_name}}.git {{project_name}}
createdb -e -U postgres -O postgres {{project_name}}
```

### Enviroment initialization

```shell
cd ~/projects/{{project_name}}
git checkout development
git pull
source ~/venvs/{{project_name}}/bin/activate
pip install -U pip
pip install -r requirements/dev.txt
```

### Data creation or reset

Only first time or if you want reset all data

```shell
dropdb -e -U postgres {{project_name}}
createdb -e -U postgres -O postgres {{project_name}}
python manage.py migrate
python manage.py createsuperuser
```

## Testing

### Enviroment initialization

```shell
cd ~/projects/{{project_name}}
source ~/venvs/{{project_name}}/bin/activate
pip install -r requirements/testing.txt
```

### Testing execution

```shell
$ python manage.py test --setting={{project_name}}.settings.testing --keepdb --parallel
$ python manage.py behave --setting={{project_name}}.settings.testing --keepdb
```
