from os import environ
from {{project_name}} import __version__
import uuid


CURRENT_ID = unicode(uuid.uuid4())


def metainfo(request):
    metainfo = {
        'uuid': CURRENT_ID,
        'version': __version__,
        'static_version': "?v={}".format(CURRENT_ID),
        'branch': environ.get('BRANCH', None)
    }
    return metainfo
