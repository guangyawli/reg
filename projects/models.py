from django.db import models
from django.contrib.auth.models import User
from idea.models import Team
from django.core.validators import MinValueValidator, MaxValueValidator


class JudgerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='評審')
    judger_realname = models.CharField(max_length=20, blank=True, verbose_name='評審姓名')
    judger_group = models.CharField(max_length=10, blank=True, verbose_name='組別')
    check_judger = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class TeamScore(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score_applicability = models.IntegerField(default=0, verbose_name='應用性', validators=[MinValueValidator(0),
                                                                                         MaxValueValidator(30)])
    score_creativity = models.IntegerField(default=0, verbose_name='創意性', validators=[MinValueValidator(0),
                                                                                      MaxValueValidator(30)])
    score_challenge = models.IntegerField(default=0, verbose_name='挑戰性', validators=[MinValueValidator(0),
                                                                                     MaxValueValidator(20)])
    score_completion = models.IntegerField(default=0, verbose_name='完成度', validators=[MinValueValidator(0),
                                                                                      MaxValueValidator(20)])
    judger_name = models.CharField(max_length=20, blank=True, verbose_name='評審名稱')
    total_score = models.IntegerField(default=0, verbose_name='隊伍總分')

    def __str__(self):
        return self.team.team_name
