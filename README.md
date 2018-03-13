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
  - check `requirements/dev.txt` to customize your virtualenv 
  - check `{{project_name}}.ini` to customize your workarea root and project root
  - and than execute `fab configure_project` into your project directory

- To merge your project with git repository execute `fab gitclone:<your_repo_git_url>`

- If you use uwsgi with emperor mode you have to create symbolic link of `{{project_name}}.ini` into vassals directory

- Check settings and urls to configure django applications

- Enjoy
