from django.urls import path
from core.views import *

urlpatterns = [
    path('', Home.as_view(), name='home')
]
