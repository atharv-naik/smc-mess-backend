from django.urls import path

from . import views


app_name = 'smc'

urlpatterns = [
    path('', views.menu, name='menu'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('menu/', views.mainMenu, name='mainMenu'),
    path('testmenu/', views.testMenu, name='testMenu'),
]