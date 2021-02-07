from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class Home(TemplateView):
    template_name = 'core/index-2.html'
    extra_context = {
        'context': "context goes here!",
        'name': "kuch nahi"
    }
