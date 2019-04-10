"""Django settings for {{project_name}} project."""

import os

SETTINGS = os.environ.get('SETTINGS', '')

if SETTINGS == '{{project_name}}.settings.testing':
    from {{project_name}}.settings.testing import *   # noqa
elif 'www/{{project_name}}_alpha' in os.getcwd():
    from {{project_name}}.settings.alpha import *   # noqa
elif 'www/{{project_name}}_beta' in os.getcwd():
    from {{project_name}}.settings.beta import *   # noqa
elif 'www/{{project_name}}' in os.getcwd():
    from {{project_name}}.settings.master import *   # noqa
else:
    from {{project_name}}.settings.local import *   # noqa
