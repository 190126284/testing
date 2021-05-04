from django.urls import path
from . import views
from musicapp.views import *

# Add URLConf
urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('signup/', register, name='signup'),
    path('logout/', views.logout_request, name='logout'),
]
