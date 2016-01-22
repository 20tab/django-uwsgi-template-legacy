from django.test import TestCase
from commons import CURRENT_ID
from commons.context_processors import metainfo


class CommonsTest(TestCase):

    def test_metainfo(self):
        assert CURRENT_ID == metainfo(None)['uuid']
