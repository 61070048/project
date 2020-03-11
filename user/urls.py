from django.contrib import admin
from django.urls import path, include
from user import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'), 
]
