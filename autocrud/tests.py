import os

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
  os.environ['DJANGO_SETTINGS_MODULE'] = 'autocrud.test_settings'

from django.http import HttpResponseBadRequest
from django.utils import unittest
from autocrud import requests
from django.core import management
from django.test.utils import setup_test_environment
import autocrud.test_settings as settings

class RequestTestCase(unittest.TestCase):
  def test_invalidOperationReturnsBadRequest(self):
    response = requests.handle_request(MockRequest(), appname="foo", modelname="foo", operation="invalid")
    self.assertEquals(type(response), HttpResponseBadRequest)

  def test_GETRequestReturnsBadRequest(self):
    response = requests.handle_request(MockRequest(method="GET"), appname="foo", modelname="foo", operation="foo")
    self.assertEquals(type(response), HttpResponseBadRequest)

class MockRequest(object):
  def __init__(self, method="POST", POST = []):
    self.method = method
    self.POST = POST

def suite():
  management.setup_environ(settings)
  setup_test_environment()
  suite = unittest.TestLoader().loadTestsFromTestCase(RequestTestCase)
  return suite