from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 基本的な認証エンドポイントは将来追加予定
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
] 