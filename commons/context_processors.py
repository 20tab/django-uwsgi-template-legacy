from os import environ
from {{ project_name }} import __version__
import uuid


def metainfo(request):
    current_id = unicode(uuid.uuid4())
    metainfo = {
        'uuid': current_id,
        'version': __version__,
        'static_version': "?v={}".format(current_id),
        'branch': environ.get('BRANCH', None)
    }
    return metainfo
