from django.contrib import admin
from .models import Account, Profile

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    list_display_links = ('first_name', 'last_name')
    readonly_fields = ('password', 'created_at', 'last_login')

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)