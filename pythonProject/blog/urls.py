from django.urls import path
from . import views  # importando dados da mesma pasta

urlpatterns = [
    path('', views.index)
]
