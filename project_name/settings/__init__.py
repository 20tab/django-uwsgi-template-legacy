import os

SETTINGS = os.environ.get('SETTINGS', '')

if SETTINGS == '{{project_name}}.settings.testing':
    from {{project_name}}.settings.testing import *   # noqa
elif 'www/{{project_name}}_alpha' in os.getcwd():
    from {{project_name}}.settings.alpha import *   # noqa
elif 'www/{{project_name}}_dev' in os.getcwd():
    from {{project_name}}.settings.develop import *   # noqa
elif 'www/{{project_name}}' in os.getcwd():
    from {{project_name}}.settings.master import *   # noqa
else:
    from {{project_name}}.settings.local import *   # noqa
