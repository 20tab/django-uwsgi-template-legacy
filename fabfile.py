from __future__ import unicode_literals

import importlib
from fabric.api import local, run, env, cd, settings as fab_settings
from fabric.contrib.console import confirm
from fabric.contrib.files import sed
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


def configure_project():
    venv = prompt(
        'Specifica il percorso della directory per il virtualenv oppure lascia vuoto per installarlo dentro {}'.format(
            VENVS_DIRNAME))
    if not venv:
        venv = VENVS_DIRNAME
    vassals = prompt('Specifica il percorso della directory per i vassals oppure lascia vuoto per usare {}'.format(
        VASSALS))
    if not vassals:
        vassals = VASSALS

    if not os.path.exists("{}/{}".format(venv, PROJECT_DIRNAME)):
        local("virtualenv {}/{}".format(venv, PROJECT_DIRNAME))
        local("{}/{}/bin/pip install -r {}/requirements.txt".format(venv, PROJECT_DIRNAME, BASE_DIR))
    if not os.path.exists('templates'):
        local('mkdir templates')
    if not os.path.exists('static'):
        local('mkdir static')
    if not os.path.exists('media'):
        local('mkdir media')
    if not os.path.exists('{}/{}.ini'.format(vassals, PROJECT_DIRNAME)):
        local('ln -s {}/uwsgiconf/locals/{}.ini {}/{}.ini'.format(BASE_DIR, PROJECT_DIRNAME, vassals, PROJECT_DIRNAME))

    how_db = prompt('Digita 1 per creare il db, 2 per scaricarlo dal server oppure lascia vuoto per non fare nulla!')
    if how_db == "1":
        create_db()
    elif how_db == "2":
        db_from_server()


def create_db():
    if confirm("Attenzione, stai creando il db. Sei sicuro di voler procedere?"):
        if "postgresql_psycopg2" in db_local['ENGINE']:
            local('createdb -h {} -p {} -U postgres {}'.format(
                db_local['HOST'], db_local['PORT'], db_local['NAME']))
            fastprint('- Database {} creato. carico il dump'.format(
                db_local['NAME']))


def run_test():
    local("coverage run ./manage.py test --settings='{{project_name}}.settings.testing'")
    local("coverage html")


def gitclone(repository):
    local('git init')
    local('flake8 --install-hook')
    local('git config flake8.strict true')
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
        fastprint("Ricordati che sincronizzando i file media e' necessario sincronizzare anche il database con il comando 'fab db_from_server'.")


def db_from_server(settings='develop'):
    server = ServerUtil(settings)
    if confirm("Attenzione, in questo modo tutti i dati presenti sul database del tuo computer verranno sovrascritti con quelli del database remoto. Sei sicuro di voler procedere?"):
        if "postgresql_psycopg2" in server.conf.DATABASES['default']['ENGINE']:
            server.get_remote_dump()
            local('psql -h {} -p {} -U postgres -c "select pg_terminate_backend(pid) from pg_stat_activity where datname = \'{}\';"'.format(
                db_local['HOST'], db_local['PORT'], db_local['NAME']))
            local('dropdb --if-exists -h {} -p {} -U postgres {}'.format(
                db_local['HOST'], db_local['PORT'], db_local['NAME']))
            fastprint('- Database {} eliminato'.format(db_local['NAME']))
            local('createdb -h {} -p {} -U postgres {}'.format(
                db_local['HOST'], db_local['PORT'], db_local['NAME']))
            fastprint('- Database {} creato. carico il dump'.format(
                db_local['NAME']))
            local('psql -h {} -p {} -U postgres -x -e -E -w -d {} -f tempdump.sql -L /dev/null'.format(
                db_local['HOST'], db_local['PORT'], db_local['NAME']))
            local('rm tempdump.sql')
        elif "sqlite" in server.conf.DATABASES['default']['ENGINE']:
            fastprint('- Engine SQLite')
            local("scp -P {} {}@{}:{}/{} {}".format(
                server.port, server.user, server.host, server.working_dir,
                server.conf.DATABASES['default']['NAME'], db_local['NAME'])
            )


def migrate_db(source='master', dest='develop'):
    server_source = ServerUtil(source)
    server_dest = ServerUtil(dest)
    if confirm("Attenzione, stai cancellando il database {} Sei sicuro di voler procedere?".format(dest.upper())):
        server_source.get_remote_dump()
        server_dest.set_remote_dump()


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

    def get_remote_dump(self):
        with fab_settings(host_string=self.host):
            with cd(self.working_dir):
                print ('- Engine Postgres')
                run("pg_dump -h {} --port={} --username={} -O {} -f tempdump.sql".format(
                    self.db['HOST'], self.db['PORT'], self.db['USER'], self.db['NAME']))
                local("scp -P {} {}@{}:{}/tempdump.sql tempdump.sql".format(
                    self.port, self.user, self.ip, self.working_dir))
                run("rm tempdump.sql")

    def set_remote_dump(self):

        if confirm("Attenzione, in questo modo tutti i dati presenti sul database {} verranno sovrascritti. Sei sicuro di voler procedere?".format(self.settings.upper())):
            with fab_settings(host_string=self.host):
                with cd(self.working_dir):
                    local("scp -P {} tempdump.sql {}@{}:{}/tempdump.sql".format(
                        self.port, self.user, self.ip, self.working_dir))
                    run('psql -h {} -p {} -U postgres -c "select pg_terminate_backend(pid) from pg_stat_activity where datname = \'{}\';"'.format(
                        self.db['HOST'], self.db['PORT'], self.db['NAME']))
                    run('dropdb --if-exists -h {} -p {} -U postgres {}'.format(
                        self.db['HOST'], self.db['PORT'], self.db['NAME']))
                    print('- Database {} eliminato'.format(self.db['NAME']))
                    run('createdb -h {} -p {} -U postgres {}'.format(
                        self.db['HOST'], self.db['PORT'], self.db['NAME']))
                    print('- Database {} creato. carico il dump'.format(
                        self.db['NAME']))
                    run('psql -h {} -p {} -U postgres -x -e -E -w -d {} -f tempdump.sql -L /dev/null'.format(
                        self.db['HOST'], self.db['PORT'], self.db['NAME']))
