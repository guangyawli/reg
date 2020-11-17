from django.contrib import admin
from accounts.models import MailServer, Emails, UserProfile
from django.contrib.auth.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_code')


class EmailsAdmin(admin.ModelAdmin):
    list_display = ('e_from', 'e_title', 'e_content', 'e_status')


class MailServerAdmin(admin.ModelAdmin):
    list_display = ('m_server', 'm_user', 'm_password')


admin.site.register(Emails, EmailsAdmin)
admin.site.register(MailServer, MailServerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
