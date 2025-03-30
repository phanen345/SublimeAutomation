
app_name = 'backoffice'
from django.contrib import admin
from django.urls import path
from backoffice import views
from backoffice.views import oauth_gmail_login, oauth_callback
# from user import views as user_views
urlpatterns = [
    path('', views.dashboard, name='navigation'),
    path('complaint/<str:operation>/', views.complaint, name='complaints'),
    path('admin_registration/', views.admin_registration, name='admin_registration'),
    path('profile/', views.profile, name='profile'),
    path('oauth/gmail/', oauth_gmail_login, name='oauth_gmail_login'),
    path('oauth/callback/', oauth_callback, name='oauth_callback'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('login/',views.login_page, name='login'),
    path('logout/',views.logout_view, name='logout_view'),
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('delete_employee', views.delete_employee, name='delete_employee'),
    # path('test/', views.test, name='test'),
    path('edit/',views.update, name='update'),
    path('complaints',views.create_complaint, name='create_complaint'),
    path('add',views.employee_add, name='employee_add'),
    
    
    
]
