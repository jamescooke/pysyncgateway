# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Database
from pysyncgateway.resource import Resource


def test(admin_client):
    """
    This indirectly tests Resource.__repr__
    """
    database = Database(admin_client, 'db')
    resource = Resource(database)
    resource.url = 'http://mockhőst/db/__Café__'

    result = unicode(resource)

    assert result == '<Resource "http://mockhőst/db/__Café__">'
