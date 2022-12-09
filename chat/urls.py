from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:class_name>/', views.class_chat, name='class'),
]