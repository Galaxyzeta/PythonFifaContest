from django.urls import path

from . import views

urlpatterns = [
    path('data', views.getFifaDataPage, name='data'),
    path('maxpages', views.getMaxDataPage, name='maxpages'),
    path('bestplayers', views.bestPlayers, name='bestplayers'),
    path('importantAbilities', views.importantAbilitites, name='importantAbilities'),
    path('', views.hello, name='hello')
]