app_name = 'user'
from django.contrib import admin
from django.urls import path
from user import views
from user.views import google_auth, google_auth_callback
# from user.views import oauth_gmail_login, oauth_callback
urlpatterns = [
    path('', views.navigation, name='navigation'),
    path('complaint/<str:operation>/', views.complaint, name='complaints'),
    path('profile/', views.profile, name='profile'),
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('logout/',views.logout_view, name='logout_view'),
    path('login/', views.login, name='login'),
    # path('change_password',views.change_password,name='change_password'),
    path('registration_user/', views.registration_user, name='registration_user'),
    #Authentication login
    # path('oauth/gmail/', oauth_gmail_login, name='oauth_gmail_login'),
    
    path('edit/',views.edit_profile, name='update'),
    # path('google_login/',views.login_with_google, name='login_with_google'),
    # path('complete/gmail_login/', views.custom_login, name='complete'),
    # path('gmail/', views.login_with_gmail, name='login_with_gmail'),
    
    
    
    path('auth/google/', google_auth, name='google_auth'),
    path('auth/google/callback/', google_auth_callback, name='google_auth_callback'),
    
]



# https://accounts.google.com/o/oauth2/auth?client_id=121742523439-s30kcv1je7lg798uen7rd4ntk1oagh39.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/user/complete/gmail_login/&state=PgNlIlTgE1FkGxspG8ZLTbybjrJC1H5V&response_type=code&scope=openid+email+profile