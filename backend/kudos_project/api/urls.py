from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/me/', views.current_user, name='current_user'),
    path('users/', views.organization_users, name='organization_users'),
    path('kudos/', views.KudoListCreateView.as_view(), name='kudos'),
    path('kudos/received/', views.received_kudos, name='received_kudos'),
    path('kudos/given/', views.given_kudos, name='given_kudos'),
]
