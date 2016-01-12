import os

if "www/{{ project_name }}" in os.getcwd():
    from {{ project_name }}.settings.master import *
elif "www/{{ project_name }}_dev" in os.getcwd():
    from {{ project_name }}.settings.develop import *
else:
    from {{ project_name }}.settings.local import *