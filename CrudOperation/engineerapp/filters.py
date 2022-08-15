from dataclasses import field
import django_filters

from .models import *


class LPFilter(django_filters.FilterSet): 
    class Meta:
        model = EngLPModel  #model that will be filtered
        fields = '__all__'  #fields that will be filtered
        exclude = ['engineer',] #fields that you don't want to be filter
