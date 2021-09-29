from django.urls import path
from . import views
urlpatterns = [
    path('user/', views.Register_Users, name='Register'),
    path('login/', views.login_user, name='Login'),
    path('logout/', views.User_logout, name='Logout'),
    path('user/<str:pk>/', views.User_info, name='user_info'),
    path('weather/id=<str:pk>/', views.weatherInformationId, name='weather-id'),
    path('weather/location=<str:pk>/', views.weatherInformationLocation, name='weather-location'),
    path('weather/condition=<str:pk>/', views.weatherInformationCondition, name='weather-condition'),
    path('weather/average=<str:pk>/', views.weatherInformationAverage, name='weather-average'),

]