"""
URL configuration for tournamentApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# tournamentApp/urls.py
from django.urls import path
from tournament.views import tournament_list, tournament_detail

urlpatterns = [
    path('api/tournaments/', tournament_list, name='tournament-list'),
    path('api/tournaments/<int:pk>/', tournament_detail, name='tournament-detail'),
]
