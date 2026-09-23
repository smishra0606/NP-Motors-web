from django.urls import path
from . import views
from billing_app.views import trigger_import
urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('create-invoice/', views.create_invoice, name='create_invoice'),
    path('invoice/<uuid:unique_bill_id>/', views.view_invoice_pdf, name='view_invoice_pdf'),
    path('secret-import-excel/', views.trigger_import, name='trigger_import'),
]
