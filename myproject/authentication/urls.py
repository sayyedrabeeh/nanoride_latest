from django.urls import path
from . import views

app_name = 'authentication'   

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('logout/',views.custom_logout_view, name='custom_logout'),

]
