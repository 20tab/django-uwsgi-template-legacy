from {{project_name}}.settings import DATABASES
import subprocess


PGDUMP = "pg_dump"
db = DATABASES['remote']

command = []
command.append(PGDUMP)
command.append("-h")
command.append(db['HOST'])
command.append("--port=%s" % db['PORT'])
command.append("--username=%s" % db['USER'])
command.append("-O")
command.append(db['NAME'])
command.append("-f")
command.append("tempdump.sql")

subprocess.call(command)
