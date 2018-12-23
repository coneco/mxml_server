from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('models/', views.models, name='models'),
    path('logs/', views.logs, name='logs')
]