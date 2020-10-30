from datetime import datetime
import os
import uuid

from django.core import validators
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# def user_readme_path(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
#     return os.path.join("readme_files", filename)

def user_readme_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/<filename>
    today = datetime.now()
    ext = filename.split('.')[-1]
    filename = '{}{}.{}'.format(instance.team_name, today, ext)
    return os.path.join("readme_files", filename)


def user_affidavit_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/<filename>
    today = datetime.now()
    ext = filename.split('.')[-1]
    filename = '{}{}.{}'.format(instance.team_name, today, ext)
    return os.path.join("affidavit_files", filename)


class Team(models.Model):
    team_name = models.CharField(max_length=40, unique=True, verbose_name='隊伍名稱')
    team_topic = models.CharField(max_length=50, verbose_name='主題')
    team_school = models.CharField(max_length=40, verbose_name='學校')
    team_teacher = models.CharField(max_length=30, verbose_name='指導教授')
    leader = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='隊長')
    video_link = models.URLField(blank=True, verbose_name='影片簡介')
    code_link = models.URLField(blank=True, verbose_name='原始碼')
    readme = models.FileField(upload_to=user_readme_path, blank=True, verbose_name='說明文件',
                              validators=[validators.FileExtensionValidator(['pdf'], message='必須為pdf格式')])
    affidavit = models.FileField(upload_to=user_affidavit_path, blank=True, verbose_name='切結書',
                                 validators=[validators.FileExtensionValidator(['pdf'], message='必須為pdf格式')])

    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='隊伍名稱')
    member_name = models.CharField(max_length=30, blank=False, verbose_name='隊員姓名')
    school_name = models.CharField(max_length=50, verbose_name='學校')
    department_name = models.CharField(max_length=30, verbose_name='系所', blank=False)
    department_grade = models.IntegerField(default=1, verbose_name='系級')
    phone_number = models.CharField(max_length=20, verbose_name='電話')
    email_addr = models.EmailField(verbose_name='信箱')
    player_num = models.IntegerField(default=1, verbose_name='隊伍人數')

    def __str__(self):
        return self.team.team_name


class Competition(models.Model):
    competition_name = models.CharField(max_length=30, verbose_name='競賽名稱', unique=True)
    percentage_applicability = models.IntegerField(default=0, verbose_name='應用性百分比')
    percentage_creativity = models.IntegerField(default=0, verbose_name='創意性百分比')
    percentage_challenge = models.IntegerField(default=0, verbose_name='挑戰性百分比')
    percentage_completion = models.IntegerField(default=0, verbose_name='完成度百分比')

    def __str__(self):
        return self.competition_name


class TeamScore(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score_applicability = models.IntegerField(default=0, verbose_name='應用性')
    score_creativity = models.FloatField(default=0, verbose_name='創意性')
    score_challenge = models.FloatField(default=0, verbose_name='挑戰性')
    score_completion = models.FloatField(default=0, verbose_name='完成度')
    judge_user = models.CharField(max_length=30, verbose_name='評審名稱')
    total_score = models.FloatField(default=0, verbose_name='隊伍總分')
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE, default='', verbose_name='競賽名稱')

    def __str__(self):
        return self.team.team_name



