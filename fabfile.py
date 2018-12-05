import configparser
import importlib
import os

from django.core.management.utils import get_random_secret_key
from fabric.api import local
from fabric.contrib.console import confirm
from fabric.operations import prompt
from fabric.state import output
from fabric.utils import fastprint

BASE_DIR = os.path.dirname(__file__)
BASE_DIRNAME = os.path.dirname(BASE_DIR)
PROJECT_DIRNAME = os.path.basename(os.path.dirname(__file__))
EMPEROR_MODE = True
VENVS = f'{BASE_DIRNAME}/venvs'
VASSALS = f'{BASE_DIRNAME}/vassals'
PY_VERSION = 'python3'
USERNAME = os.getlogin()
SECRET_FILE = f'{BASE_DIR}/{PROJECT_DIRNAME}/settings/secret.py'
SECRET_KEY = get_random_secret_key()

output['everything'] = True


def init():
    if not confirm('Is your project virtualenv activated?'):
        fastprint('Activate your virtualenv and run the fab command again')
        return
    EMPEROR_MODE = confirm('Do you want to configure your uWSGI vassal in emperor mode? (no=stand-alone)')
    if EMPEROR_MODE:
        vassals = prompt(f'We will use "{VASSALS}" as the directory for the vassals, or specify the path:') or VASSALS
    username = prompt(f'Enter the database user name:')
    password = prompt(f'Enter the database user password:')
    local(f'pip install -r {BASE_DIR}/requirements/dev.txt')
    if not os.path.exists('templates'):
        local('mkdir templates')
    if not os.path.exists('static'):
        local('mkdir static')
    if not os.path.exists('media'):
        local('mkdir media')
    if EMPEROR_MODE and not os.path.exists(f'{vassals}/{PROJECT_DIRNAME}.ini'):
        local(f'cp {BASE_DIR}/uwsgiconf/locals/{PROJECT_DIRNAME}.ini {BASE_DIR}/uwsgiconf/locals/{USERNAME}.ini')
        local(f'ln -s {BASE_DIR}/uwsgiconf/locals/{USERNAME}.ini {vassals}/{PROJECT_DIRNAME}.ini')
    if not os.path.exists(f'{SECRET_FILE}'):
        local(f'cp {SECRET_FILE}.template {SECRET_FILE}')
        local(f'sed -i -e "s/password/{password}/g;s/secretkey/{SECRET_KEY}/g;s/username/{username}/g" {SECRET_FILE}')
    create_db()
    fastprint('\n\n*** WARNING ***\n\n')
    fastprint('a) Check uwsgiconf/locals/{USERNAME}.ini and verify that you have the correct python plugin\n')
    fastprint('b) Check the uwsgiconf/remotes/globlal.ini file and verify that you have the correct python plugin\n')
    fastprint('c) Check the uwsgiconf/remotes/alpha.ini file and make sure the domain name is correct\n')
    fastprint('d) Configure the deploy/hosts file with server data\n')
    fastprint('e) Configure the deploy/alpha.yaml file with the correct data\n')
    fastprint('f) Configure the file by {PROJECT_DIRNAME}/settings/testing.py with the correct data\n')


def get_db():
        with open(SECRET_FILE, 'r') as f:
            config_string = '[secret]\n' + f.read()
        config = configparser.ConfigParser()
        config.read_string(config_string)
        db_name = config.get('secret', 'DATABASES_DEFAULT_NAME')
        db_host = config.get('secret', 'DATABASES_DEFAULT_HOST')
        db_port = config.get('secret', 'DATABASES_DEFAULT_PORT')
        db_user = config.get('secret', 'DATABASES_DEFAULT_USER')
        return db_name, db_host, db_port, db_user


def create_db():
    if confirm('Pay attention, you are creating the Postgresql db. Are you sure you want to proceed?'):
        db_name, db_host, db_port, db_user = get_db()
        local(f"createdb -e -h {db_host} -p {db_port} -U {db_user} -O {db_user} {db_name}")


def drop_db():
    if confirm('Warning, you are deleting the db. Are you sure you want to proceed?'):
        db_name, db_host, db_port, db_user = get_db()
        local(f"dropdb -e -h {db_host} -p {db_port} -U {db_user} {db_name}")


def gitclone(repository):
    local('git init')
    local('flake8 --install-hook git')
    local('git config flake8.strict true')
    local('git add -A')
    local('git commit -m "first commit"')
    local(f'git remote add origin {repository}')
    local('git push -u origin master')


def media_from_server(settings='develop'):
    """
    Copy all media files from the server defined by the settings passed as an argument.
    """
    server = ServerUtil(settings)
    if confirm(f'Do you want to overwrite local files in /media/ with those on the {settings.upper()} server?'):
        server_string = f'{server.user}@{server.ip}:{server.working_dir}'
        local(f'rsync -av --progress --inplace -e="ssh -p{server.port}" {server_string}/media/ ./media/')
        fastprint('Remember that synchronizing the media files also requires synchronizing the database.')


class ServerUtil(object):

    def __init__(self, settings):
        self.settings = settings
        self.conf = importlib.import_module(f'{{project_name}}.settings.{settings}')
        self.user = self.conf.HOST_USER
        self.ip = self.conf.HOST_IP
        self.port = self.conf.HOST_PORT
        self.host = f'{self.user}@{self.ip}:{self.port}'
        self.working_dir = self.conf.WORKING_DIR
        self.db = self.conf.DATABASES['default']
