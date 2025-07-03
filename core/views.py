from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import TestModel

def home(request):
    test = TestModel(name="Speedy Test")
    test.save()
    return HttpResponse("MongoDB Connected and Test Saved!")