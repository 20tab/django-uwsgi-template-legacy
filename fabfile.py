import importlib
from fabric.api import local, run, env, cd
from fabric.contrib.console import confirm
from fabric.utils import fastprint
from fabric.state import output
from fabric.operations import prompt
from {{project_name}}.settings.local import DATABASES as LOCAL_DB
import os

BASE_DIR = os.path.dirname(__file__)
PROJECT_DIRNAME = os.path.basename(os.path.dirname(__file__))
VENVS_DIRNAME = "{}/venvs".format(os.path.dirname(BASE_DIR))
VASSALS = "{}/vassals".format(os.path.dirname(BASE_DIR))

output['everything'] = True
db_local = LOCAL_DB['default']


def init():
    venv = prompt(
        'Specifica il percorso della directory per il virtualenv oppure lascia vuoto per installarlo dentro {}'.format(
            VENVS_DIRNAME))
    if not venv:
        venv = VENVS_DIRNAME
    vassals = prompt('Specifica il percorso della directory per i vassals oppure lascia vuoto per usare {}'.format(
        VASSALS))
    if not vassals:
        vassals = VASSALS

    py_version = prompt('Sara\' usato python3 di default. Altrimenti specifica la versione corretta (Es. python2.7)') or 'python3'

    if not os.path.exists("{}/{}".format(venv, PROJECT_DIRNAME)):
        local("virtualenv -p {} {}/{}".format(py_version, venv, PROJECT_DIRNAME))
        local("{}/{}/bin/pip install -r {}/requirements/dev.txt".format(venv, PROJECT_DIRNAME, BASE_DIR))
    if not os.path.exists('templates'):
        local('mkdir templates')
    if not os.path.exists('static'):
        local('mkdir static')
    if not os.path.exists('media'):
        local('mkdir media')
    if not os.path.exists('{}/{}.ini'.format(vassals, PROJECT_DIRNAME)):
        local('ln -s {}/uwsgiconf/locals/{}.ini {}/{}.ini'.format(BASE_DIR, PROJECT_DIRNAME, vassals, PROJECT_DIRNAME))

    how_db = prompt('Digita 1 per creare il db oppure lascia vuoto per non fare nulla!')
    if how_db == "1":
        create_db()

    fastprint('\n\n*** PERFETTO ***\n\n')
    fastprint('a) Controlla il file focustask.ini e assicurati che il sia installato il plugin python corretto\n')
    fastprint(
        'b) Controlla il file develop.ini e master.ini e assicurati che il sia installato il plugin python corretto\n')
    fastprint('c) Configura il file deploy/hosts con i dati del server\n')
    fastprint('d) Configura il file deploy/alpha.yaml con i dati corretti\n')
    fastprint('e) Configura il file settings/testing.py con i dati corretti')


def create_db():
    if confirm("Attenzione, stai creando il db. Sei sicuro di voler procedere?"):
        if "postgresql" in db_local['ENGINE']:
            local('createdb -h {} -p {} -U postgres {}'.format(
                db_local['HOST'], db_local['PORT'], db_local['NAME']))
            fastprint('- Database {} creato.'.format(db_local['NAME']))



def gitclone(repository):
    local('git init')
    local('git add -A')
    local("git commit -m 'first commit'")
    local('git remote add origin {}'.format(repository))
    local('git push -u origin master')


def media_from_server(settings='develop'):
    """
    Copia tutti i file media dal server definito dal settings passato come argomento
    """
    server = ServerUtil(settings)
    if confirm("Stai sovrascrivendo tutti i file contenuti in /media/ in locale con quelli sul server {}. Vuoi procedere?".format(settings.upper())):
        local("rsync -av --progress --inplace --rsh='ssh -p{}' {}@{}:{}/media/ ./media/".format(
            server.port, server.user, server.ip, server.working_dir))
        fastprint("Ricordati che sincronizzando i file media e' necessario sincronizzare anche il database.")



class ServerUtil(object):

    def __init__(self, settings):
        self.settings = settings

        self.conf = importlib.import_module('{{project_name}}.settings.{}'.format(settings))
        self.user = self.conf.HOST_USER
        self.ip = self.conf.HOST_IP
        self.port = self.conf.HOST_PORT
        self.host = "{}@{}:{}".format(self.user, self.ip, self.port)
        self.working_dir = self.conf.WORKING_DIR
        self.db = self.conf.DATABASES['default']
