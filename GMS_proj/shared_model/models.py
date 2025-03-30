#  This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ComplaintStatus(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'complaint_status'
        app_label = 'shared_model'


class Department(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'department'
        app_label = 'shared_model'


class Designation(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'designation'
        app_label = 'shared_model'


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    profile_type_id = models.IntegerField()
    profile_type=models.CharField(max_length=50)
    designation_id = models.IntegerField()
    department_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateField()
    last_login = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'profile'
        app_label = 'shared_model'

class CreateComplaint(models.Model):
    id=models.IntegerField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    subject = models.CharField(max_length=400)
    message = models.CharField(max_length=1000)
    current_handler = models.CharField(max_length=35)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    image=models.URLField()
    class Meta:
        managed = True
        db_table = 'complaint'
        app_label = 'shared_model'

class ComplaintMessage(models.Model):
    id=models.IntegerField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    complaint_id=models.IntegerField()
    class Meta:
        managed = True
        db_table = 'complaint_message'
        app_label = 'shared_model'



class UserRegistration(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    
    class Meta:
        managed = True
        db_table = 'user_registration'
        app_label = 'shared_model'


class AdminRegistration(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    
    class Meta:
        managed = True
        db_table = 'admin_registration'
        app_label = 'shared_model'