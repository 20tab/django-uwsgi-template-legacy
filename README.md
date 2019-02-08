{{project_name}}
================

This is a [Django](https://docs.djangoproject.com/en/{{docs_version}}/) template with custom configuration. It requires [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) as application server 
> **NOTE** : for OSX check [uwsgi-emperor-mode](https://github.com/20tab/uwsgi-emperor-mode) to configure your own local server with emperor.

## Prerequisite

Set you environment. We kindly suggest updating pip to the latest version and using a virtualenv  to wrap all your work.

### Virtualenv

Use one this options to create an empty virtualenv with the right python version, and activate it:

> **NOTE** : replace `venvs` with your actual virtualenv directory

* use virtualenv for python2:
  ```shell
  $ pip install --user -U pip virtualenv
  $ virtualenv --python=python3 ~/venvs/{{project_name}}
  $ source ~/venvs/{{project_name}}/bin/activate
  ```

* use venv for python3:
  ```shell
  $ pip3 install --user -U pip
  $ python3 -m venv ~/venvs/{{project_name}}
  $ source ~/venvs/{{project_name}}/bin/activate
  ```

* use virtualenvwrapper for an easier workflow:
  ```shell
  $ pip install --user -U pip virtualenvwrapper
  $ mkvirtualenv --python=python3 {{project_name}}
  $ workon {{project_name}}
  ```

### Packages

To use this template you need the latest Django and Invoke version installed.

```shell
({{project_name}}) $ pip install -U django invoke
```

## Project

### New

To start a new project with this template:

```shell
({{project_name}}) $ django-admin.py startproject --template https://www.20tab.com/template/ -e cfg,ini,md,py,yaml,template -n Makefile {{project_name}}
```

### Clone

To clone an existing project created with this template:

```shell
({{project_name}}) $ git clone https://example.com/{{project_name}}.git
```

## Configuration

1. Enter the folder of your **project** *(es: ~/projects/{{project_name}})*

2. To configure the project execute **init task** and answer all questions:

    ```shell
    ({{project_name}}) $ inv init
    ```

3. To merge your project with git repository execute:

   ```shell
   ({{project_name}}) $ inv gitclone <your_repo_git_url>
   ```

4. Check `{{project_name}}/settings/*.py` and `{{project_name}}/urls.py` to configure your project

5. Enjoy

## Data Setup

### Database reset

To execute only if you want reset all data:

```shell
({{project_name}}) $ inv dropdb
({{project_name}}) $ inv createdb
({{project_name}}) $ python manage.py migrate
```

### Superuser creation

Execute after the first installation if you need a super user for your admin

```shell
({{project_name}}) $ python manage.py createsuperuser
```

## Requirements

### Check 

To list all outdated installed packages execute:

```shell
({{project_name}}) $ pip list -o
```

### Edit

To add/remove packages or modify their versions edit `requirements/*.ini` files and to update all related `requirements/*.txt` execute:

```shell
({{project_name}}) $ make pip
```

To update sub-dependencies *(es: packages listed in `install_requires`)* use 'p' option as below:

```shell
({{project_name}}) $ make pip p='-P pytz'
```

### Update

To install the updated `requirements/dev.txt` in your local virtualenv execute:

```shell
({{project_name}}) $ make dev
```

## Testing

To run test and behave with coverage execute:

```shell
({{project_name}}) $ make test
```

> **NOTE** : [django-bdd-toolkit](https://github.com/20tab/django-bdd-toolkit) to use behave in a regular django project.

## Frontend building

The command installs dependencies and compiles the frontend code into static files that are used in the views.

```shell
({{project_name}}) $ make npm
```

## Continuous Integration

To setup the build in a Continuous Integration environment *(eg: jenkins)* use this code:

```shell
make ci PASSWORD=<db_user_password> SECRETKEY=<django_secret_key>
```

## Deploy

To deploy your project in the alpha instance you need to rename the deploy/alpha.yaml.template and deploy/hosts.template file 
and edit with your correct credentials.

"alpha" environment is just an example. For every environment you need, you can duplicate alpha configurations to other 
files (eg. beta.yaml or production.yaml) and correspondent Makefile commands. 

Both the remote server and the ci system need node.js to build static files by default. If you don't need any module bundler
you can modify Makefile ci command and deploy/deploy.yaml deleting useless commands.

To initialize the alpha instance you have to execute the next two commands:

```shell
({{project_name}}) $ make initalpha
({{project_name}}) $ make alpha
```

To update your alpha instance after some code updates you have to execute the next command only:

```shell
({{project_name}}) $ make alpha
```