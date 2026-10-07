from django.urls import path
from SecAuth_App import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.SecAuth_views, name='register_url'),
    path('login/', views.SecAuth_login_view, name='login_url'),
    path('dashboard/', views.SecAuth_dashboard_view, name='dashboard_url'),
    path('logout/', views.SecAuth_logout_view, name='logout_url'),
]
