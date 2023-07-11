from django.urls import path

from . import views

urlpatterns = [
    path('balance/<str:roll>', views.getBalance, name='getBalance'),
    path('items/', views.getItems, name='getItems'),
    path('accounts/', views.getAccounts, name='getAccounts'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_funds/', views.addFunds, name='addFunds'),
    path('history/<str:roll>', views.getHistory, name='getHistory'),
    path('account-statement/<str:roll>', views.emailStatement, name='emailStatement'),
    path('', views.getRoutes, name='getRoutes')
]