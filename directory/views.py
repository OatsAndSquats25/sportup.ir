from django.shortcuts import render
from django.views.generic import ListView, DetailView

from models import club

# Create your views here.
class listAllItems(ListView):
    template_name = "directory/listall.html"
    model = club

class itemDetail(DetailView):
    template_name = "directory/item.html"
    model = club