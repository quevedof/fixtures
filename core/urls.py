from django.urls import path
from .views import *

urlpatterns = [
    path("", FootballView.as_view(), name='football'),
    path("tennis/", TennisView.as_view(), name='tennis'),
    path("formula1/", Formula1View.as_view(), name='formula1'),
    path("lol/", LeagueOfLegendsView.as_view(), name='lol'),
    path("valorant/", ValorantView.as_view(), name='valorant'),


]
