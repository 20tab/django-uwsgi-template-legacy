import configparser
import getpass
import importlib
import os
import pathlib
import sys

from django.core.management.utils import get_random_secret_key
from invoke import task

BASE_DIR = os.path.dirname(__file__)
BASE_DIRNAME = os.path.dirname(BASE_DIR)
PROJECT_DIRNAME = os.path.basename(os.path.dirname(__file__))
EMPEROR_MODE = True
VASSALS = f'{BASE_DIRNAME}/vassals'
USERNAME = os.getlogin()
SECRET_FILE = f'{BASE_DIR}/{PROJECT_DIRNAME}/settings/secret.py'
SECRET_KEY = get_random_secret_key()


@task
def init(c):
    try:
        VENV_ROOT = str(pathlib.Path(os.environ['VIRTUAL_ENV']).parent).replace("/", "\/")  # noqa
    except KeyError:
        print('Activate your virtualenv and run the inv command again')
        return
    EMPEROR_MODE = confirm('Do you want to configure your uWSGI vassal in emperor mode? (no=stand-alone)')
    if EMPEROR_MODE:
        vassals = input(f'We will use "{VASSALS}" as the directory for the vassals, or specify the path: ') or VASSALS
        bonjour = confirm('Do you want to use Bonjour for OSX (Yes) or Avahi for Linux (No)? ')
        if bonjour:
            ZEROCONF = 'bonjour'
            ZEROOPTS = 'name=%(project_name).local,cname=localhost'
        else:
            ZEROCONF = 'avahi'
            ZEROOPTS = '%(project_name).local'
    python_plugin = input(
        f'Specify python plugin to configure uwsgi or blank to use default value (python3): ') or "python3"
    username = input(f'Enter the database user name: ')
    password = getpass.getpass(f'Enter the database user password: ')
    print('Compiling pip file in requirements')
    c.run('make pip')
    print('Installing libraries in requirements')
    c.run('make dev')
    if not os.path.exists('templates'):
        print('Making templates directory')
        c.run('mkdir templates')
    if not os.path.exists('static'):
        print('Making static directory')
        c.run('mkdir static')
    if not os.path.exists('media'):
        print('Making media directory')
        c.run('mkdir media')
    ini_dir = f'{BASE_DIR}/uwsgiconf/locals'
    PYVERSION = f"{sys.version_info[0]}.{sys.version_info[1]}"
    WORKAREA_ROOT = BASE_DIRNAME.replace("/", "\/")  # noqa
    print('Generating uwsgi user file')
    if EMPEROR_MODE and not os.path.exists(f'{vassals}/{PROJECT_DIRNAME}.ini'):
        c.run(f'cp {ini_dir}/emperor.ini.template {ini_dir}/{USERNAME}.ini')
        c.run((
            f'sed -i".bak" -e "s/USERNAME/{USERNAME}/g;s/ZEROCONF/{ZEROCONF}/g;s/ZEROOPTS/{ZEROOPTS}/g;" {ini_dir}/'
            f'{USERNAME}.ini'))
        c.run(f'ln -s {BASE_DIR}/uwsgiconf/locals/{USERNAME}.ini {vassals}/{PROJECT_DIRNAME}.ini')
    else:
        c.run(f'cp {ini_dir}/standalone.ini.template {ini_dir}/{USERNAME}.ini')
    c.run(f'sed -i".bak" -e "s/plugin = python3/plugin = {python_plugin}/g;" {ini_dir}/{USERNAME}.ini')
    c.run(f'sed -i".bak" -e "s/WORKAREA_ROOT/{WORKAREA_ROOT}/g;" {ini_dir}/{USERNAME}.ini')
    c.run(f'sed -i".bak" -e "s/PYVERSION/{PYVERSION}/g;" {ini_dir}/{USERNAME}.ini')
    c.run(f'sed -i".bak" -e "s/VENV_ROOT/{VENV_ROOT}/g;" {ini_dir}/{USERNAME}.ini')
    print('Installing secret file in settings')
    if not os.path.exists(f'{SECRET_FILE}'):
        c.run(f'cp {SECRET_FILE}.template {SECRET_FILE}')
        c.run((
            f'sed -i".bak" -e "s/password/{password}/g;s/secretkey/{SECRET_KEY}/g;s/username/{username}/g"'
            f' {SECRET_FILE}'
        ))
    else:
        c.run(f'sed -i".bak" -e "s/password/{password}/g;s/username/{username}/g" {SECRET_FILE}')
    createdb(c)
    print('*** Next steps ***')
    print(f'a) Check the uwsgiconf/locals/{USERNAME}.ini and verify that you have the correct python plugin')
    print('b) Check the uwsgiconf/remotes/globlal.ini file and verify that you have the correct python plugin')
    print('c) Check the uwsgiconf/remotes/alpha.ini file and make sure the domain name is correct')
    print('d) Configure the deploy/hosts file with server data')
    print('e) Configure the deploy/alpha.yaml file with the correct data')
    print(f'f) Configure the file by {PROJECT_DIRNAME}/settings/testing.py with the correct data')
    if EMPEROR_MODE:
        c.run(f"python -m webbrowser -t http://{PROJECT_DIRNAME}.local/")


@task
def createdb(c):
    if confirm('Pay attention, you are creating the Postgresql db. Are you sure you want to proceed?'):
        db_name, db_host, db_port, db_user = get_db()
        c.run(f"createdb -e -h {db_host} -p {db_port} -U {db_user} -O {db_user} {db_name}")


@task
def dropdb(c):
    if confirm('Warning, you are deleting the db. Are you sure you want to proceed?'):
        db_name, db_host, db_port, db_user = get_db()
        c.run(f"dropdb -e -h {db_host} -p {db_port} -U {db_user} {db_name}")


@task
def gitinit(c, git_repository_url):
    c.run(f'sed -i".bak" -e "s/<git_repository_url>/{git_repository_url}/g;" README.md')
    c.run('git init')
    c.run('flake8 --install-hook git')
    c.run('git config flake8.strict true')
    c.run('git add -A')
    c.run('git commit -m "Initial commit"')
    c.run(f'git remote add origin {git_repository_url}')
    c.run('git push -u origin master')


@task
def media_from_server(c, settings='develop'):
    """
    Copy all media files from the server defined by the settings passed as an argument.
    """
    server = ServerUtil(settings)
    if confirm(f'Do you want to overwrite local files in /media/ with those on the {settings.upper()} server?'):
        server_string = f'{server.user}@{server.ip}:{server.working_dir}'
        c.run(f'rsync -av --progress --inplace -e="ssh -p{server.port}" {server_string}/media/ ./media/')
        print('Remember that synchronizing the media files also requires synchronizing the database.')


@task
def restart(c):
    c.run(f'touch uwsgiconf/locals/{USERNAME}.ini')


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


class ServerUtil(object):

    def __init__(self, settings):
        self.settings = settings
        self.conf = importlib.import_module(f'pyromatest.settings.{settings}')
        self.user = self.conf.HOST_USER
        self.ip = self.conf.HOST_IP
        self.port = self.conf.HOST_PORT
        self.host = f'{self.user}@{self.ip}:{self.port}'
        self.working_dir = self.conf.WORKING_DIR
        self.db = self.conf.DATABASES['default']


# NOTE: originally cribbed from fab 1's contrib.console.confirm
def confirm(question, assume_yes=True):
    """
    Ask user a yes/no question and return their response as a boolean.

    ``question`` should be a simple, grammatically complete question such as
    "Do you wish to continue?", and will have a string similar to ``" [Y/n] "``
    appended automatically. This function will *not* append a question mark for
    you.

    By default, when the user presses Enter without typing anything, "yes" is
    assumed. This can be changed by specifying ``affirmative=False``.

    .. note::
        If the user does not supplies input that is (case-insensitively) equal
        to "y", "yes", "n" or "no", they will be re-prompted until they do.

    :param str question: The question part of the input.
    :param bool assume_yes:
        Whether to assume the affirmative answer by default. Default value:
        ``True``.

    :returns: A `bool`.
    """
    # Set up suffix
    if assume_yes:
        suffix = 'Y/n'
    else:
        suffix = 'y/N'
    # Loop till we get something we like
    # TODO: maybe don't do this? It can be annoying. Turn into 'q'-for-quit?
    while True:
        # TODO: ensure that this is Ctrl-C friendly, ISTR issues with
        # raw_input/input on some Python versions blocking KeyboardInterrupt.
        response = input('{0} [{1}] '.format(question, suffix))
        response = response.lower().strip()  # Normalize
        # Default
        if not response:
            return assume_yes
        # Yes
        if response in ['y', 'yes']:
            return True
        # No
        if response in ['n', 'no']:
            return False
        # Didn't get empty, yes or no, so complain and loop
        err = "I didn't understand you. Please specify '(y)es' or '(n)o'."
        print(err, file=sys.stderr)
