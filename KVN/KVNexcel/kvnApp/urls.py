from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', views.home, name='home'),
    path('adv', views.adv,name='adv'),
    path('hyb', views.hyb, name='hyb'),
    path('cart', views.cart, name='cart'),
    path('Login',views.Login, name = 'Login'),
    path('Register',views.Register, name = 'Register'),
    path('Logout',views.Logout, name = 'Logout'),
    path('activateuser/<uidb64>/<token>',views.ActivateUser, name = 'ActivateUser'),
    
    path('resetpassword/',auth_views.PasswordResetView.as_view(template_name='ResetPassword.html'), name = 'reset_password'),
    path('resetpassword/sent/',auth_views.PasswordResetDoneView.as_view(template_name='ResetPasswordSent.html'), name = 'password_reset_done'),
    path('resetpassword/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='ResetPasswordConfirm.html'), name = 'password_reset_confirm'),
    path('resetpassword/success/',auth_views.PasswordResetCompleteView.as_view(template_name='ResetPasswordSuccess.html'), name = 'password_reset_complete'),

    path('dashboard/', login_required(views.Dashboard), name='Dashboard'),
    path('pricing',views.pricing, name='pricing'),
    path('basic', views.basic_courses, name='basic_courses'),
    path('advanced', views.advanced_courses, name='advanced_courses'),
    path('initiate_payment/',(views.initiate_payment), name='initiate_payment'),
    path('R_advanced', views.R_advanced, name='R_advanced'),
    path('R_basic', views.R_basic, name='R_basic'),
    path('Excel_shortcuts', views.Excel_shortcuts, name='Excel_shortcuts'),
    path('Conditional_formating', views.Conditional_formating, name='Conditional_formating'),
    path('Maths',views.Maths, name='Maths'),
    
    path('formulas', views.formulas, name='formulas'),
    path('pivotal', views.pivotal, name='pivotal'),
    path('analysis', views.analysis, name='analysis'),
    path('powerbi', views.powerbi, name='powerbi'),
    path('visual', views.visual, name='visual'),
    path('arrays', views.arrays, name='arrays'),
    path('user_details',views.user_details, name='user_details'),

    path('basic_dashboard', views.basic_dashboard, name='basic_dashboard'),
    path('advanced_dashboard', views.advanced_dashboard, name='advanced_dashboard'),
    path('playground', views.playground, name='playground'),
    path('corp', views.corp, name='corp'),


    


    
]