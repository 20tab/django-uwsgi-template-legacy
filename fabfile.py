import importlib
import os

from fabric.api import local
from fabric.contrib.console import confirm
from fabric.operations import prompt
from fabric.state import output
from fabric.utils import fastprint

from {{project_name}}.settings.local import DATABASES as LOCAL_DB

BASE_DIR = os.path.dirname(__file__)
BASE_DIRENAME = os.path.dirname(BASE_DIR)
PROJECT_DIRNAME = os.path.basename(os.path.dirname(__file__))
VENVS = f'{BASE_DIRENAME}/venvs'
VASSALS = f'{BASE_DIRENAME}/vassals'
PY_VERSION = 'python3'

output['everything'] = True
db_local = LOCAL_DB['default']


def init():
    venvs = prompt(f'Installeremo il virtualenv dentro "{VENVS}", oppure specifica il percorso:') or VENVS
    vassals = prompt(f'Useremo "{VASSALS}" come directory per i vassals, oppure specifica il percorso:') or VASSALS
    py_version = prompt(f'Useremo {PY_VERSION}, oppure specifica un\'altra versione (es: python2.7):') or PY_VERSION
    if not os.path.exists(f'{venvs}/{PROJECT_DIRNAME}'):
        local(f'virtualenv -p {py_version} {venvs}/{PROJECT_DIRNAME}')
        local(f'{venvs}/{PROJECT_DIRNAME}/bin/pip install -U pip')
        local(f'{venvs}/{PROJECT_DIRNAME}/bin/pip install -r {BASE_DIR}/requirements/dev.txt')
    else:
        local(f'. {venvs}/{PROJECT_DIRNAME}/bin/activate')
    if not os.path.exists('templates'):
        local('mkdir templates')
    if not os.path.exists('static'):
        local('mkdir static')
    if not os.path.exists('media'):
        local('mkdir media')
    if not os.path.exists('{}/{}.ini'.format(vassals, PROJECT_DIRNAME)):
        local(f'ln -s {BASE_DIR}/uwsgiconf/locals/{PROJECT_DIRNAME}.ini {vassals}/{PROJECT_DIRNAME}.ini')
    create_db()
    fastprint('\n\n*** ATTENZIONE ***\n\n')
    fastprint('a) Controlla il file {{project_name}}.ini e assicurati che sia installato il plugin python corretto\n')
    fastprint('b) Controlla il file globlal.ini e assicurati che sia installato il plugin python corretto\n')
    fastprint('c) Configura il file deploy/hosts con i dati del server\n')
    fastprint('d) Configura il file deploy/alpha.yaml con i dati corretti\n')
    fastprint('e) Configura il file settings/testing.py con i dati corretti')


def create_db():
    if confirm("Attenzione, stai creando il db. Sei sicuro di voler procedere?"):
        if "postgresql" in db_local['ENGINE']:
            local(f"createdb -h {db_local['HOST']} -p {db_local['PORT']} -U postgres -O postgres {db_local['NAME']}")
            fastprint(f"- Database {db_local['NAME']} creato.")


def gitclone(repository):
    local('git init')
    local('flake8 --install-hook git')
    local('git config flake8.strict true')
    local('git add -A')
    local("git commit -m 'first commit'")
    local(f'git remote add origin {repository}')
    local('git push -u origin master')


def media_from_server(settings='develop'):
    """
    Copia tutti i file media dal server definito dal settings passato come argomento.
    """
    server = ServerUtil(settings)
    if confirm(f'Vuoi sovrascrivere i file locali in /media/ con quelli sul server {settings.upper()}?'):
        server_string = f'{server.user}@{server.ip}:{server.working_dir}'
        local(f"rsync -av --progress --inplace -e='ssh -p{server.port}' {server_string}/media/ ./media/")
        fastprint("Ricordati che sincronizzando i file media e' necessario sincronizzare anche il database.")


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
