from django.db import models

# Create your models here.

from mongoengine import Document, StringField, FloatField

class TestModel(Document):
    name = StringField()

class MenuItem(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    image_data = StringField()
    def __str__(self):
        return self.name
