{{project_name}}
================

This is a [Django](https://www.djangoproject.com/) template with custom configuration. It requires [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) as application server.

## Prerequisite

To use this template you need latest Django and Fabric3 version.

```
sudo pip3 install -U django fabric3
```

## Installation

To start a new project with this template:

```
django-admin.py startproject --template=https://github.com/20tab/twentytab_project/zipball/master --extension=py,ini,txt,md,yaml,coveragerc,template -n Makefile,hosts {{project_name}}
```

## Configuration

- To configure project with virtualenv and required empty directories: 
  - check `requirements/dev.ini` to customize your virtualenv and then execute:
      ```
    $ make pip
    ````
  - export your local DB password and execute the setup command:
      ```
    $ export PASSWORD=<password>
    $ make setup
    ````
  - check `uwsgiconf/local/<username>.ini` to customize your local uWSGI settings
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

