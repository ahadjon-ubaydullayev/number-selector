from django.urls import path
from number.views import index


urlpatterns = [
    path('api/', index, name='handler'),
  
   
]
