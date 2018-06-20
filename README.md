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
django-admin.py startproject --template=https://github.com/20tab/twentytab_project/zipball/master --extension=py,ini,txt,md,yaml,coveragerc,template -n Makefile,hosts {{project_name}}
```

## Configuration

- To configure project with virtualenv and required empty directories: 
  - check `requirements/dev.ini` to customize your virtualenv 
  - check `{{project_name}}.ini` to customize your workarea root and project root
  - copy `{{project_name}}/settings/secret.py.template` to `{{project_name}}/settings/secret.py.template` and:
    - set `SECRET_KEY` with
      ```
      $  python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
      ```
    - (optional) set `DATABESE_*` and `EMAIL_*` values
  - execute `fab init` into your project directory

- To merge your project with git repository execute `fab gitclone:<your_repo_git_url>`

- If you use uwsgi with emperor mode you have to create symbolic link of `{{project_name}}.ini` into vassals directory

- Check settings and urls to configure django applications

- Enjoy

## Data Setup

Data creation or reset, to execute only first time or if you want reset all data.

```shell
$ fab drop_db
$ fab create_db
```

Table and superuser creation.

```shell
$ python manage.py migrate
$ python manage.py createsuperuser
```

## Testing

Environment initialization, and execution of behave and test with coverage.

```shell
$ make test
```
