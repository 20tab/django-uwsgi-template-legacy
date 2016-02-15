from django.test import TestCase
from commons.context_processors import metainfo, CURRENT_ID


class CommonsTest(TestCase):

    def test_metainfo(self):
        assert CURRENT_ID == metainfo(None)['uuid']
