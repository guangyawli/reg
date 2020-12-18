from django.db import models
from django.contrib.auth.models import User
from idea.models import Team


class JudgerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='審查教師')
    judger_group = models.CharField(max_length=10, blank=True, verbose_name='組別')
    check_judger = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class TeamScore(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score_applicability = models.IntegerField(default=0, verbose_name='應用性')
    score_creativity = models.FloatField(default=0, verbose_name='創意性')
    score_challenge = models.FloatField(default=0, verbose_name='挑戰性')
    score_completion = models.FloatField(default=0, verbose_name='完成度')
    judge_user = models.ForeignKey(JudgerProfile, on_delete=models.CASCADE, verbose_name='評審名稱')
    total_score = models.FloatField(default=0, verbose_name='隊伍總分')

    def __str__(self):
        return self.team.team_name
