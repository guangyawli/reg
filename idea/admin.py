from django.contrib import admin

# Register your models here.
from .models import Team, TeamMember, TeamScore, Competition


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_topic', 'team_school', 'team_teacher', 'leader', 'readme', 'affidavit',
                    'video_link', 'code_link')
    list_filter = ("team_name", "team_school")
    search_fields = ("team_name", "team_teacher")
    ordering = ("team_name",)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'member_name', 'school_name', 'department_name', 'department_grade', 'phone_number',
                    'email_addr')
    list_filter = ('team', "member_name", "department_name")
    ordering = ('team', "id",)


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('competition_name', 'percentage_applicability', 'percentage_creativity', 'percentage_challenge',
                    'percentage_completion')
    list_filter = ('competition_name',)
    ordering = ('competition_name',)


class TeamScoreAdmin(admin.ModelAdmin):
    list_display = ('team', 'score_applicability', 'score_creativity', 'score_challenge', 'score_completion',
                    'judge_user', 'total_score', 'competition')
    list_filter = ('competition', 'team')
    ordering = ('competition',)


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(TeamScore, TeamScoreAdmin)
