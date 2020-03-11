from django.contrib import admin
from django.urls import path
from event import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:event_id>/', views.detail ,name='detail'),
    path('payment/<int:event_id>/', views.payment, name='payment'),
    path('event/', views.query_event, name='event'),
    path('category/', views.query_category, name='category')
]