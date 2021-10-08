from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_invoice, name='create_invoice'),
    path('edit/<int:pk>/', views.details_invoice, name='details_invoice'),
    path('delete/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
    path('export-data/', views.export_csv, name='export_csv'),
    path('filter-status/', views.filter_status, name='filter_status')
    
]