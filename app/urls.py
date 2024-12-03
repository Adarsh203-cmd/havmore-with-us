from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
#from app.views import ResetPasswordView
#from .views import ChangePasswordView

urlpatterns = [
    path("login/",views.loginview,name="loginn"),
    path("loginu",views.userlogin,name="login"),
    path("signup/",views.signup,name="sign"),
    path("forgotv",views.forgotview,name="forgot"),
    #path("cpassword/",views.ChangePassword,name="pchange"),
    #path("forgotp",views.ForgetPassword,name="fpassword"),
    path("register/",views.registeruser,name="register"),
    path("menu/",views.menuview,name='menu'),
    path("views",views.indexview,name='index'),
    path("view",views.index1,name='controls'),
    path("itemadd/",views.itemadd,name="itemadd"),
    path("edititem/<int:pk>",views.edititem,name="edit"),
    path("update/<int:pk>",views.updatedata,name="update"),
    path("item/",views.item,name="item"),
    path("show/",views.show,name="show"),
    path("userinfo/",views.usershow,name="users"),
    path("iteminfo/",views.userpage,name="items"),
    path('delete/<int:d>',views.deleteitem,name="delete"),
    path('aboutus/',views.aboutus,name="about"),
    path('filtered_items/', views.filter_item_list, name='filter_item_list'),
    path('place_order/', views.place_order, name='place_order'),
    #path("orders/",views.orderspage,name="order"),
    #path('distributor-order-handler/', views.distributor_order_handler, name='distributor_order_handler'),
    path('orders/',views.orders, name='orders'),
    path('orders/update_status/<int:order_id>/', views.update_status, name='update_status'),
    #path('generate-invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
   #path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('corders/', views.display_orders, name='corders'),
    path('payment/confirm/<int:order_id>/', views.payment_confirm, name='payment_confirm'),
    path('payment/<int:order_id>/', views.payment_form, name='payment_form'),
    path('paysuccess/<str:invoice_number>/', views.paysuccess, name='paysuccess'),
    path('payment/process/<int:order_id>/', views.payment, name='payment'),
    path('generate_bill_pdf/<int:order_id>/', views.generate_bill_pdf, name='generate_bill_pdf'),
    path('feedback/',views.feedback, name='feedback'),
    path('feedbackk/', views.feedbackk, name='feedbackk'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('update-password/', views.update_password, name='update_password'),
    path('report/',views.report,name='report'),
    path("loginr/",views.loginrview,name='loginreport'),
    #path('send-otp/', views.send_otp, name='send_otp'),
    #path('verify-otp/', views.verify_otp, name='verify_otp'),
    #path('change-password/', views.change_password, name='change_password'),
    #path('generate_bill_pdff/<int:order_id>/', views.generate_bill, name='generate_bill'),   
    #path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='views'), name='logout'),
    #preset


    #path('process_selected_items/', views.process_selected_items, name='process_selected_items'),
    #path('place_order/', views.place_order, name='place_order'),
    #path('order/page',views.orderpage,name='orderp'),
    #path('itemorder/',views.itemorder,name="itemo"),
   #path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
   #path('', TemplateView.as_view(template_name="preset.html"), name='preset'),
   #path('password-reset/', ResetPasswordView.as_view(), name='passwordr'),
   #path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),  
]