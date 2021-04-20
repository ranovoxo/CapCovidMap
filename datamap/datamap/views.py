from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from . import texas


def index(requst):
    return render(request, template_name = 'index.html')


def texas_map():
    plot_div = texas.texas_map()
    return {'texas_map' : plot_div}

def mapspage(request):
    plot_div = texas.texas_counties()
    return render(request, "maps.html",context = {'texas_counties' : plot_div})

# Create your views here.
