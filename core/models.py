from django.db import models

# Create your models here.

from mongoengine import Document, StringField, FloatField , EmailField

class TestModel(Document):
    name = StringField()

class MenuItem(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    image_data = StringField()
    def __str__(self):
        return self.name

class Admin_User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

class SiteUser(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    mobile = StringField(required=True, unique=True)
