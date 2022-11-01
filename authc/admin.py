from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import GroupAdmin as GroupAdminDefault
from .models import User
from .forms import GroupAdminForm

# https://youtu.be/XJU9vRARkGo

admin.site.register(User)
admin.site.unregister(User)

class AccountAdmin(UserAdmin):
    list_display = ('email','username','is_staff')
    search_fields = ('email','username',)
    readonly_fields=('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, AccountAdmin)

# https://github.com/Microdisseny/django-groupadmin-users/blob/main/groupadmin_users/forms.py

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(GroupAdminDefault):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)