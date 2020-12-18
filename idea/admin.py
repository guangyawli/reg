from django.contrib import admin

# Register your models here.
from .models import Team, TeamMember


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_topic', 'team_school', 'team_teacher', 'leader', 'readme', 'affidavit',
                    'video_link', 'code_link', 'team_group')
    list_filter = ("team_school", "team_group", 'stu_check')
    search_fields = ("team_name", "team_teacher")
    ordering = ("team_name", "team_group", 'stu_check')


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'member_name', 'school_name', 'department_name', 'department_grade', 'phone_number',
                    'email_addr')
    list_filter = ('team', "member_name", "department_name")
    ordering = ('team', "id",)


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)

