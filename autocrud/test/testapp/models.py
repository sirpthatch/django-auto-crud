from django.db import models

class TestModel(models.Model):
  string_field = models.CharField(max_length=256)
  number_field = models.IntegerField()
  boolean_field = models.BooleanField()
  float_field = models.FloatField()
  
