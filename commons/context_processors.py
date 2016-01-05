from os import environ
from {{ project_name }} import __version__
import uuid


def metainfo(request):
    metainfo = { 
        'uuid': unicode(uuid.uuid4()),
        'version': __version__,
        'static_version': "?v={}".format(uuid),
        'branch': environ['BRANCH']
    } 
    return metainfo
