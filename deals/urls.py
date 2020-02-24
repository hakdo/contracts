from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('partners/', views.partners, name='partners'),
    path('contracts/<str:status>/', views.index, name='contracts'),
    path('contracts/contract/<int:pk>/', views.contract_detail, name='contract_detail'),
    path('partners/<int:pk>/', views.partner_detail, name='partner_contracts'),
    path('search/', views.search, name='search'),
    path('contracts/new', views.new_contract, name='new_contract'),
    path('contracts/contract/<int:pk>/edit', views.edit_contract, name='edit_contract'),
]