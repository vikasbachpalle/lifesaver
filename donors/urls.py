from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),                 # optional root redirection
    path('registerdonor/', views.registerdonor, name='registerdonor'),
    path('searchdonor/', views.searchdonor, name='searchdonor'),
    path('donors/', views.donors_list, name='donors_list'),     # all donors list (recent)
    path('login/', views.donor_login, name='donor_login'),
    path('logout/', views.donor_logout, name='donor_logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]
