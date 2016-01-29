from __future__ import unicode_literals

from fabric.api import local, run, env, cd
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

output['everything'] = False
port = '22'
host = ''
env.hosts = ['%s:%s' % (host, port)]
project_dir = 'www/{{project_name}}'
prod_project_dir = 'www/{{project_name}}'

templates_dir = 'templates'
static_dir = 'static'
analysis_dir = 'analysis'

db_local = LOCAL_DB['default']


def configure_project():
    output['everything'] = True
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
    # TODO da implementare db_from_server e create_db con una configurazione migliore
    if how_db == "1":
        create_db()
    elif how_db == "2":
        # db_from_server()
        print('TODO: db_from_server')


def run_test():
    output['everything'] = True
    local("coverage run ./manage.py test --settings='{{ project_name }}.settings.testing'")
    local("coverage html")


def gitclone(repository):
    output['everything'] = True
    local('git init')
    local('flake8 --install-hook')
    local('git config flake8.strict true')
    local('git add -A')
    local("git commit -m 'first commit'")
    local('git remote add origin {}'.format(repository))
    local('git push -u origin master')


def media_from_server(debug=True):
    if debug:
        output['everything'] = True
    if confirm("Stai sovrascrivendo tutti i file contenuti in /media/ in locale con quelli sul server. Vuoi procedere? "):
        local("rsync -av --progress --inplace --rsh='ssh -p%s' %s:%s/media/ ./media/" % (port, host, project_dir))
        fastprint("Ricordati che sincronizzando i file media e' necessario sincronizzare anche il database con il comando 'fab db_from_server'.")


def db_from_server(debug=True, settings='develop'):
    if debug:
        output['everything'] = True
    if confirm("Attenzione, in questo modo tutti i dati presenti sul database del tuo computer verranno sovrascritti con quelli del database remoto. Sei sicuro di voler procedere?"):
        with cd(project_dir):
            if "postgresql_psycopg2" in db_local['ENGINE']:
                print ('- Engine Postgres')
                run("python dbdump.py")
                local("scp -P %s %s:%s/tempdump.sql tempdump.sql" % (port, host, project_dir))
                run("rm tempdump.sql")
                local('psql -h %s -p %s -U postgres -c "select pg_terminate_backend(pid) from pg_stat_activity where datname = \'%s\';"' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                local('dropdb --if-exists -h %s -p %s -U postgres %s' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                print ('- Database %s eliminato' % db_local['NAME'])
                local('createdb -h %s -p %s -U postgres %s' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                print ('- Database %s creato. carico il dump' % db_local['NAME'])
                if debug:
                    local('psql -h %s -p %s -U postgres -x -e -E -w -d %s -f tempdump.sql -L /dev/null' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                else:
                    local('psql -h %s -p %s -U postgres --output=/dev/null -q -t -w -d %s -f tempdump.sql -L /dev/null' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                local('rm tempdump.sql')
            elif "sqlite" in db_remote['ENGINE']:
                fastprint('- Engine SQLite')
                local("scp -P %s %s:%s/%s %s" % (port, host, project_dir, db_remote['NAME'], db_local['NAME']))


def create_db(debug=True):
    if debug:
        output['everything'] = True
    if confirm("Attenzione, stai creando il db. Sei sicuro di voler procedere?"):
        if "postgresql_psycopg2" in db_local['ENGINE']:
            local('createdb -h %s -p %s -U postgres %s' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
            print ('- Database %s creato. carico il dump' % db_local['NAME'])
