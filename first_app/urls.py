from django.urls import path
from . import views

 
urlpatterns=[
   path("",views.home_page),
   path("add-network",views.add_network)
]

