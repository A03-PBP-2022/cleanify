from django.contrib import admin
from .models import Location

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
	list_display = ['pk', 'location', 'date']
	list_display_links = ['pk', 'location', 'date']
	ordering = ['pk']
admin.site.register(Location, LocationAdmin)
