from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('travels', views.travels),
    path('travels/destination/<destination_id>', views.show),
    path('travels/add', views.add),
    path('create', views.create),
    path('join/<trip_id>', views.join),
    path('remove/<trip_id>', views.remove),
    path('destroy/<trip_id>', views.destroy),
    path('logout', views.logout),
]