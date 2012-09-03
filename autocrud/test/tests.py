import json
import os

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
  os.environ['DJANGO_SETTINGS_MODULE'] = 'autocrud.test.test_settings'

from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import unittest
from autocrud import requests
from django.core import management
from django.test.utils import setup_test_environment
import autocrud.test.test_settings as settings

management.setup_environ(settings)
setup_test_environment()
management.call_command('syncdb',noinput=True)


class RequestTestCase(unittest.TestCase):
  def test_invalidOperationReturnsBadRequest(self):
    response = requests.handle_request(MockRequest(), appname="testapp", modelname="foo", operation="invalid")
    self.assertEquals(type(response), HttpResponseBadRequest)

  def test_GETRequestReturnsBadRequest(self):
    response = requests.handle_request(MockRequest(method="GET"), appname="testapp", modelname="foo", operation="foo")
    self.assertEquals(type(response), HttpResponseBadRequest)

  def test_operationOnInvalidModelReturnsBadRequest(self):
    response = requests.handle_request(MockRequest(method="POST"), appname="testapp", modelname="foo", operation="read")
    self.assertEquals(type(response), HttpResponseBadRequest)

  def test_canCreateNewModel(self):
    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":42,
                "string_field":"test",
                "boolean_field":True,
                "float_field":42.1}),
      appname="testapp",
      modelname="TestModel",
      operation="create")
    self.assertNotEquals(type(response), HttpResponseBadRequest)
    try:
      int(response.content)
    except:
      self.fail("Expecting ID in response, got [%s]"%response.content)

  def test_creationFailsIfPassInInvalidType(self):
    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":"this is not a number",
                "string_field":"test",
                "boolean_field":True,
                "float_field":42.1}),
      appname="testapp",
      modelname="TestModel",
      operation="create")
    self.assertEquals(type(response), HttpResponseBadRequest)

  def test_canReadModelWithFullParameters(self):
    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":42,
                "string_field":"test",
                "boolean_field":True,
                "float_field":42.1}),
      appname="testapp",
      modelname="TestModel",
      operation="create")

    id = int(response.content)

    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"id":id}),
      appname="testapp",
      modelname="TestModel",
      operation="read")

    response_dictionary = json.loads(response.content)
    self.assertEquals(response_dictionary,{u'id':id,u'number_field':42,u'string_field':u'test',u'boolean_field':True,u'float_field':42.1})

  def test_canUpdateModelSingleField(self):
    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":42,
                "string_field":"test",
                "boolean_field":True,
                "float_field":42.1}),
      appname="testapp",
      modelname="TestModel",
      operation="create")

    id = int(response.content)

    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"id":id,
                "number_field":43}),
      appname="testapp",
      modelname="TestModel",
      operation="update")

    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"id":id}),
      appname="testapp",
      modelname="TestModel",
      operation="read")

    response_dictionary = json.loads(response.content)
    self.assertEquals(response_dictionary[u'number_field'],43)

  def test_canUpdateModelMultipleFields(self):
    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":42,
                "string_field":"test",
                "boolean_field":True,
                "float_field":42.1}),
      appname="testapp",
      modelname="TestModel",
      operation="create")

    id = int(response.content)

    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"id":id,
                "number_field":43,
                "float_field":43.1}),
      appname="testapp",
      modelname="TestModel",
      operation="update")

    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"id":id}),
      appname="testapp",
      modelname="TestModel",
      operation="read")

    response_dictionary = json.loads(response.content)
    self.assertEquals(response_dictionary[u'number_field'],43)
    self.assertEquals(response_dictionary[u'float_field'],43.1)

  def test_updateFailsIfNoId(self):
    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":42,
                "string_field":"test",
                "boolean_field":True,
                "float_field":42.1}),
      appname="testapp",
      modelname="TestModel",
      operation="create")

    id = int(response.content)

    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":43}),
      appname="testapp",
      modelname="TestModel",
      operation="update")

    self.assertEquals(type(response),HttpResponseBadRequest)

  def test_canDeleteModel(self):
    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"number_field":42,
                "string_field":"test",
                "boolean_field":True,
                "float_field":42.1}),
      appname="testapp",
      modelname="TestModel",
      operation="create")

    id = int(response.content)

    response = requests.handle_request(
      MockRequest(
        method="POST",
        POST = {"id":id}),
      appname="testapp",
      modelname="TestModel",
      operation="delete")

    response = bool(response.content)
    self.assertTrue(response)

class MockRequest(object):
  def __init__(self, method="POST", POST = {}):
    self.method = method
    self.POST = POST