from django.urls import re_path,path
from dankano.productapp import views as view


urlpatterns = [
    re_path(r'^display_invoices/',view.displayInvoice, name='display_invoices'),
    re_path(r'^debit_invoices/',view.displayDebitInvoice, name='debit_invoices'),
    re_path(r'^create_invoice/',view.createInvoice, name='create_invoice'),
    re_path(r'^create-build-invoice/(?P<inv_id>\d+)/',view.createBuildInvoice, name='create-build-invoice'),
    re_path(r'^edit_invoice/(?P<inv_id>\d+)/',view.editInvoice, name='edit_invoice'),
    re_path(r'^delete_invoice/(?P<inv_id>\d+)/',view.deleteInvoice, name='delete_invoice'),
    re_path(r'^display_products/(?P<inv_id>\d+)/',view.displayProduct, name='display_products'),  
    re_path(r'^edit_product/(?P<prd_id>\d+)/(?P<inv_id>\d+)',view.editProduct, name='edit_product'),
    re_path(r'^delete_product/(?P<prd_id>\d+)/',view.deleteProduct, name='delete_product'), 
    re_path(r'^sales_history/',view.salesHistory, name='sales_history'),
    re_path(r'^view_reciept/(?P<inv_id>\d+)/',view.viewReciept, name='view_reciept'),
    re_path(r'^view_waybill/(?P<inv_id>\d+)/',view.viewWaybill, name='view_waybill'),

]