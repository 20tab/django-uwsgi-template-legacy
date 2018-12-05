{{project_name}}
================

This is a [Django](https://www.djangoproject.com/) template with custom configuration. It requires [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) as application server.

## Prerequisite

Set you environment. We kindly suggest updating pip to the latest version and using a virtualenv  to wrap all your work.

Use one this option to create an empty virtualenv with the right python version, and activate it:

* use virtualenv for python2:
  ```shell
  $ pip install --user -U pip virtualenv
  $ virtualenv --python=python3 ~/venvs/{{project_name}}_env
  $ source ~/venvs/{{project_name}}_env/bin/activate
  ```

* use venv for python3:
  ```shell
  $ pip3 install --user -U pip
  $ python3 -m venv ~/venvs/{{project_name}}_env
  $ source ~/venvs/{{project_name}}_env/bin/activate
  ```

* use virtualenvwrapper for an easier workflow:
  ```shell
  $ pip install --user -U pip virtualenvwrapper
  $ mkvirtualenv --python=python3 {{project_name}}_env
  $ workon {{project_name}}_env
  ```

To use this template you need the latest Django and Fabric3 version installed.

```shell
({{project_name}}_env) $ pip install django fabric3
```

## Installation

To start a new project with this template:

```shell
({{project_name}}_env) $ django-admin.py startproject --template=https://github.com/20tab/twentytab_project/zipball/master --extension=py,ini,txt,md,yaml,coveragerc,template -n Makefile,hosts {{project_name}}
```

## Configuration

- Enter the root folder of your project

- To configure the project:

  - execute fabfile into your project directory:
    ```shell
    ({{project_name}}_env) $ fab init
    ```

  - check `requirements/dev.ini` to customize your virtualenv and `requirements/common.ini` to check the version of Django, and then execute:
    ```shell
    ({{project_name}}_env) $ make pip
    ```

  - check `uwsgiconf/local/<username>.ini` to customize your local uWSGI settings
  *(mainly comment and uncomment lines for emperor (plus bonjour or avahi) or stand-alone mode)*

  - check the default db parameters into `{{project_name}}/settings/secret.py`

- To merge your project with git repository execute:
  ```shell
  ({{project_name}}_env) $ fab gitclone:<your_repo_git_url>
  ```

- Check settings and urls to configure django applications

- Enjoy

## Data Setup

### Database reset

To execute only if you want reset all data:

```shell
({{project_name}}_env) $ fab drop_db
({{project_name}}_env) $ fab create_db
({{project_name}}_env) $ python manage.py migrate
```

### Superuser creation

```shell
({{project_name}}_env) $ python manage.py createsuperuser
```

## Requirements

### Check 

List outdated packages:

```shell
({{project_name}}_env) $ pip list -o
```

### Edit

Add or edit packages in your `requirements/*.ini` files and execute:

```shell
({{project_name}}_env) $ make pip
```

To update sub-dependencies in all generated requirements use 'p' option:

```shell
({{project_name}}_env) $ make pip p='-P pytz'
```

### Update

Install the updated requirements in your virtualenv:

```shell
({{project_name}}_env) $ make dev
```

## Testing

Execute of test and behave with coverage.

```shell
({{project_name}}_env) $ make test
```
