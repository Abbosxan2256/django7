from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, IntegerField, ForeignKey, CASCADE, DateTimeField
from django_ckeditor_5.fields import CKEditor5Field


class Vacancies(Model):
    title = CharField(max_length=255)
    price = IntegerField()
    qualification = IntegerField()
    address = CharField(max_length=255)
    description = CKEditor5Field('Text', config_name='extends')
    created_at = DateTimeField(auto_now_add=True)
    employer = ForeignKey('apps.User', CASCADE)


class User(AbstractUser):
    pass
