twentytab_project
=================

This is a django template with custom configuration. It requires uwsgi as application server

## Installation

To start a new project with this template:

```
django-admin.py startproject --template=https://github.com/20tab/twentytab_project/zipball/master -e py -e ini -e txt <project_name>
```

## Configuration

- To configure project with virtualenv and required empty directories: 
  - check requirements.txt to customize your virtualenv 
  - check <project_name>.ini to customize your workarea root and project root
  - and than:
```
fab configure_project
```
into your project directory.

- To merge your project with git repository:

```
fab gitclone:your_repo_path
```

- If you use uwsgi with emperor mode you have to create symbolic link of yourproject.ini into vassals directory

- Check settings.py and urls.py to configure django applications

- Enjoy
