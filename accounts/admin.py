from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import MailServer, Emails, UserProfile
from django.contrib.auth.models import User

# Register your models here.


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_code')


class EmailsAdmin(admin.ModelAdmin):
    list_display = ('e_title', 'e_content', 'e_time')
    search_fields = ("e_status", "e_title", 'e_content')
    ordering = ("-e_time",)


class MailServerAdmin(admin.ModelAdmin):
    list_display = ('m_server', 'm_user', 'm_password')


admin.site.register(Emails, EmailsAdmin)
admin.site.register(MailServer, MailServerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
