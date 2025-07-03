from django.db import models

# Create your models here.

from mongoengine import Document, StringField

class TestModel(Document):
    name = StringField()
