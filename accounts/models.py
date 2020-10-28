from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class UserProfile(models.Model):
  check_code = models.CharField(max_length=10, blank=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)


class Emails(models.Model):
  e_from = models.CharField(max_length=50, blank=False, default='推動大學程式設計教學 <admin@coding101.tw>')
  e_title = models.CharField(max_length=100, blank=False, default='default_title')
  e_content = RichTextField(blank=True, null=True)
  e_status = models.CharField(max_length=50, blank=True)


class MailServer(models.Model):
  m_server = models.CharField(max_length=50, blank=False, default='mail.gandi.net')
  m_user = models.CharField(max_length=50, blank=False, default='admin@coding101.tw')
  m_password = models.CharField(max_length=30, blank=False, default='default_password')
