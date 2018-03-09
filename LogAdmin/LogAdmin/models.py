# coding=utf-8
from django.db import models

class Host(models.Model):
    HID = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    secret = models.CharField(max_length=30)

    def __unicode__(self):
        return self.hostname

    def __str__(self):
        return self.hostname

class Project(models.Model):
    PID = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=30)
    createtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.pname

    def __str__(self):
        return self.pname

class AppType(models.Model):
    TID = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=30,unique=True)

class Application(models.Model):
    AID = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=30 ,unique = True)
    host = models.ForeignKey(Host)
    logpath = models.CharField(max_length=50)
    project = models.ForeignKey(Project)
    apptype = models.ForeignKey(AppType)
    def __unicode__(self):
        return self.aname

    def __str__(self):
        return self.aname





# class LogType(models.Model):
#     TID = models.AutoField(primary_key=True)
#     typename = models.CharField(max_length=30)
#
#     def __unicode__(self):
#         return self.typename
#
#     def __str__(self):
#         return self.typename
#
# class Log(models.Model):
#     LID = models.AutoField(primary_key=True)
#     lname = models.CharField(max_length=30)
#     application = models.ForeignKey(Application)
#     logtype = models.ForeignKey(LogType)
#
#     def __unicode__(self):
#         return self.lname
#
#     def __str__(self):
#         return self.lname












