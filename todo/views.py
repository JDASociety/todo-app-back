from django.shortcuts import render
from rest_framework import viewsets
from .models import TodoModel
from .serializers import TodoSerializer


# Create your views here.

class TodoModelViewSet(viewsets.ModelViewSet):
    queryset = TodoModel.objects.all()
    serializer_class = TodoSerializer
