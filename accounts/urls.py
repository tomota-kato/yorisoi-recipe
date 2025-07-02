from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 簡易版API
    path('login/', views.login_api, name='login_api'),
    path('logout/', views.logout_api, name='logout_api'),
] 