from django.db import models
from django.utils.translation import ugettext as T


class NetworkSite(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=250, verbose_name=T("Path to projects"), default="/home")
    folder_name = models.CharField(max_length=50, verbose_name=T("Project folder name"))
