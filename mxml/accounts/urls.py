from django.urls import path

from . import views

urlpatterns = [
    path('github_login/', views.github_login, name='github_login'),
    path('github_auth/', views.github_auth, name='github_auth'),

    path('logout/', views.log_out, name='logout')
]