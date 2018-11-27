{{project_name}}
================

This is a [Django](https://www.djangoproject.com/) template with custom configuration. It requires [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) as application server.

## Prerequisite

Set you environment. We kindly suggest updating pip to the lates versione and using virtualenv to wrap all your work.

Eg: update pip and virtualenv, then create an empty virtualenv with the right python version, and activate it

```shell
    $ sudo pip install -U pip virtualenv
```
then
```shell
    $ virtualenv --python=python3 path/to/venvs/myvenv
    $ source path/to/venvs/myvenv/bin/activate
```
    or with virtualenvwrapper
```shell
    $ mkvirtualenv --python=python3 myvenv
```

To use this template you need the latest Django and Fabric3 version installed.

```shell
(myvenv)$ pip install django fabric3
```

## Installation

To start a new project with this template:

```
(myvenv)$ django-admin.py startproject --template=https://github.com/20tab/twentytab_project/zipball/master --extension=py,ini,txt,md,yaml,coveragerc,template -n Makefile,hosts {{project_name}}
```

## Configuration

- Enter the root folder of your project

- To configure the project:

  - check `requirements/dev.ini` to customize your virtualenv and `requirements/common.ini` to check the Django versione, then execute:
    ```shell
    (myvenv)$ make setup
    ```

  - check `uwsgiconf/local/<username>.ini` to customize your local uWSGI settings; mainly comment and uncomment lines for emperor (plus bonjour or avahi) or stand-alone mode

  - check the default db parameters into {{project_name}}/settings/secret.py.template file

  - execute `fab init` into your project directory

- To merge your project with git repository execute `fab gitclone:<your_repo_git_url>`

- If you use uwsgi with emperor mode you have to create symbolic link of `{{project_name}}.ini` into vassals directory

- Check settings and urls to configure django applications

- Enjoy

## Data Setup

### Database reset

To execute only if you want reset all data:

```shell
$ fab drop_db
$ fab create_db
$ python manage.py migrate
```

### Superuser creation

```shell
$ python manage.py createsuperuser
```

### To update virtualen

Add the packages on your requirements/\*.ini file

```shell
$ make pip
```


## Testing

Environment initialization, and execution of behave and test with coverage.

```shell
$ source ~/venvs/{{project_name}}/bin/activate
```

or

```shell
$ workon {{project_name}}
```

and

```shell
$ make test
```

after

```shell
$ make dev
```
