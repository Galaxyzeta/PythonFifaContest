from django.urls import path

from . import views

urlpatterns = [
    path('data', views.getFifaDataPage, name='data'),
    path('maxpages', views.getMaxDataPage, name='maxpages'),
    path('bestplayers', views.bestPlayers, name='bestplayers'),
    path('importantAbilities', views.importantAbilitites, name='importantAbilities'),
    path('team', views.bestTeam, name='bestTeam'),
    path('', views.hello, name='hello'),
    path('feature', views.featureRank, name='feature'),
    path('scatter', views.scatterPot, name='scatter')
]
