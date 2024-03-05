from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Complaint(models.Model):
    profile_id = models.IntegerField()
    subject = models.CharField(max_length=40)
    message = models.CharField(max_length=1000)
    current_handler = models.CharField(max_length=35)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        
        db_table = 'complaint'


class ComplaintMessage(models.Model):
    profile_id = models.IntegerField()
    message = models.CharField(max_length=255)
    media = models.CharField(max_length=255)
    created_at = models.DateField()
    updated_at = models.DateField()

    class Meta:
        
        db_table = 'complaint_message'


class ComplaintStatus(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        
        db_table = 'complaint_status'


class Department(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        
        db_table = 'department'


class Designation(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        
        db_table = 'designation'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        
        db_table = 'django_session'


class Profile(models.Model):
    name = models.CharField(max_length=27)
    mobile = models.IntegerField()
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    profile_type_id = models.IntegerField()
    designation_id = models.IntegerField()
    department_id = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()

    class Meta:
        
        db_table = 'profile'


class ProfileType(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        
        db_table = 'profile_type'