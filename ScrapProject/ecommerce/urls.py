from django.contrib import admin
from django.urls import path
from ecom import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('alogout', LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),
    path('slogout', LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),  
    path('clogout', LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),     
    path('logout', LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view,name='contactus'),
    path('search', views.search_view,name='search'),
    path('csearch', views.csearch_view,name='csearch'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('view-feedback', views.view_feedback_view,name='view-feedback'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('view-seller', views.view_seller_view,name='view-seller'),
    path('view-customer', views.view_customer_view,name='view-customer'),
    
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('delete-seller/<int:pk>', views.delete_seller_view,name='delete-seller'),    
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),

    path('admin-products', views.admin_products_view,name='admin-products'),
    path('admin-add-product', views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),

    path('admin-stocks', views.admin_stocks_view,name='admin-stocks'),
    path('admin-add-stock', views.admin_add_stock_view,name='admin-add-stock'),
    path('delete-stock/<int:pk>', views.delete_stock_view,name='delete-stock'),
    path('update-stock/<int:pk>', views.update_stock_view,name='update-stock'),


    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),


    path('customersignup', views.customer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    path('ccustomer-home', views.ccustomer_home_view,name='ccustomer-home'),
    path('my-order', views.my_order_view,name='my-order'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),
    path('download-yearwise', views.download_yearwise_view,name='download-yearwise'),
    path('download-catwise', views.download_catwise_view,name='download-catwise'),    
    path('download-namewise', views.download_namewise_view,name='download-namewise'),
    path('download-datewise', views.download_datewise_view,name='download-datewise'),
    
    path('sellersignup', views.seller_signup_view),
    path('sellerlogin', LoginView.as_view(template_name='ecom/sellerlogin.html'),name='sellerlogin'),
    path('seller-home', views.seller_home_view,name='seller-home'),
    path('cseller-home', views.cseller_home_view,name='cseller-home'),    
    path('smy-profile', views.smy_profile_view,name='smy-profile'),
    path('sedit-profile', views.sedit_profile_view,name='sedit-profile'),
    path('seller-dashboard', views.seller_dashboard_view,name='seller-dashboard'),
    path('ssearch', views.ssearch_view,name='ssearch'),
    path('scsearch', views.scsearch_view,name='scsearch'),
    path('ysearch', views.ysearch_view,name='ysearch'),    
    path('dsearch', views.dsearch_view,name='dsearch'),   
    
    path('seller-products', views.seller_products_view,name='seller-products'),
    path('seller-add-product', views.seller_add_product_view,name='seller-add-product'),
    path('sdelete-product/<int:pk>', views.sdelete_product_view,name='sdelete-product'),
    path('supdate-product/<int:pk>', views.supdate_product_view,name='supdate-product'),
    path('ndownload/<int:pk>', views.ndownload_view,name='ndownload'),
    path('cdownload/<int:pk>', views.cdownload_view,name='cdownload'),
    path('ydownload/<int:pk>', views.ydownload_view,name='ydownload'),    
    path('ddownload/<int:pk>', views.ddownload_view,name='ddownload'),    
    
    
    
    path('seller-stocks', views.seller_stocks_view,name='seller-stocks'),
    path('seller-add-stock', views.seller_add_stock_view,name='seller-add-stock'),
    path('sdelete-stock/<int:pk>', views.sdelete_stock_view,name='sdelete-stock'),
    path('supdate-stock/<int:pk>', views.supdate_stock_view,name='supdate-stock'),


    path('seller-view-booking', views.seller_view_booking_view,name='seller-view-booking'),
    path('sdelete-order/<int:pk>', views.sdelete_order_view,name='sdelete-order'),
    path('supdate-order/<int:pk>', views.supdate_order_view,name='supdate-order'),


    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),
    path('info/<int:product_id>/', views.info_page, name='info_page'),

]
