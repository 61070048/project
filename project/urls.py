from django.contrib import admin
from django.urls import path, include
from event import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('', include('event.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
