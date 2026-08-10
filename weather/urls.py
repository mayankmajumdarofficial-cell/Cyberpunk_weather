from django.urls import path
from . import views
#connecting the url path
urlpatterns = [
    path('', views.index, name='index'),
]
