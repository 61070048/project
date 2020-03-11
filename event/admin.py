from django.contrib import admin
from event.models import Event, Category
# Register your models here.

1
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_name', 'event_date', 'event_time', 'ticket_price', 'ticket_amount', 'category']
admin.site.register(Event, EventAdmin)
admin.site.register(Category)