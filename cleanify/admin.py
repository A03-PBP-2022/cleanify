from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cleanify.models import User

admin.site.register(User)


class AccountAdmin(UserAdmin):
	list_display = ('email','username','is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('id',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.unregister(User)
admin.site.register(User, AccountAdmin)


# link referensi : https://youtu.be/XJU9vRARkGo