import json
from django.db import models
from django.http import HttpResponseBadRequest, HttpResponse

def handle_request(request, appname=None, modelname=None, operation=None):
  if request.method is not 'POST':
    return HttpResponseBadRequest()
  all_models = models.get_models(models.get_app(appname))

  model = None
  for model in all_models:
    if modelname == model._meta.object_name.lower():
      break
  
  operation = str(operation.lower())

  if operation == 'create':
    return handle_create(request, model)
  if operation == 'read':
    return handle_read(request, model)
  if operation == 'update':
    return handle_update(request, model)
  if operation == 'delete':
    return handle_delete(request, model)

def handle_create(request, model=None):
  instance = model()
  for param in request.POST:
    setattr(instance, param, request.POST[param])
  instance.save()
  return HttpResponse(instance.id)

def handle_read(request, model=None):
  id = request.POST["id"]
  instance = model.objects.get(id=id)
  fields = model._meta.fields

  dict = {}
  for field in fields:
    dict[field.name] = getattr(instance,field.name)
  
  return HttpResponse(json.dumps(dict))

def handle_update(request, model=None):
  id = request.POST["id"]
  instance = model.objects.get(id=id)
  for param in request.POST:
    if param == "id":
      continue
    setattr(instance, param, request.POST[param])
  instance.save()
  return HttpResponse(instance.id)

def handle_delete(request, model=None):
  id = request.POST["id"]
  instance = model.objects.get(id=id)
  instance.delete()

  return HttpResponse()

