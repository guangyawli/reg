from django.contrib import admin
from projects.models import TeamScore, JudgerProfile, FinalTeamScore


class TeamScoreAdmin(admin.ModelAdmin):
    list_display = ('team', 'score_applicability', 'score_creativity', 'score_challenge', 'score_completion',
                    'judger_name', 'total_score')
    list_filter = ('team',)
    ordering = ('team', 'total_score')


class JudgerProfileAdmin(admin.ModelAdmin):
    list_display = ('judger_realname', 'judger_group', 'user', 'check_judger')
    list_filter = ('check_judger',)
    ordering = ('judger_group',)


class FinalTeamScoreAdmin(admin.ModelAdmin):
    list_display = ('team', 'score_applicability', 'score_creativity', 'score_challenge', 'score_completion',
                    'total_score')
    list_filter = ('team',)
    ordering = ('team', 'total_score')


admin.site.register(TeamScore, TeamScoreAdmin)
admin.site.register(JudgerProfile, JudgerProfileAdmin)
admin.site.register(FinalTeamScore, FinalTeamScoreAdmin)


