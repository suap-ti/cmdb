from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.db.models import Model, TextChoices
from django.db.models import CharField, PositiveIntegerField, TextField, DateField, URLField, EmailField, BooleanField, DateTimeField
from django.db.models import ForeignKey, CASCADE, PROTECT, RESTRICT, SET, SET_NULL, SET_DEFAULT, DO_NOTHING
from django.contrib.auth.models import AbstractUser
# from django_markdown.models import MarkdownField


class StringField(CharField):
    def __init__(self, verbose_name, max_length=250, *args, **kwargs):
        super().__init__(verbose_name=verbose_name, max_length=max_length, *args, **kwargs)


class NullStringField(StringField):
    def __init__(self, verbose_name, max_length=250, null=True, blank=True, *args, **kwargs):
        super().__init__(verbose_name=verbose_name, max_length=max_length, null=True, blank=True, *args, **kwargs)


class FK(ForeignKey):
    def __init__(self, verbose_name, to, on_delete=CASCADE, 
                 related_name=None, related_query_name=None, limit_choices_to=None, 
                 parent_link=False, to_field=None, db_constraint=True, **kwargs):
        super().__init__(to, on_delete, related_name, related_query_name, 
                         limit_choices_to, parent_link, to_field, db_constraint, verbose_name=verbose_name, **kwargs)


class NullFK(ForeignKey):
    def __init__(self, verbose_name, to, on_delete=CASCADE,  
                 related_name=None, related_query_name=None, limit_choices_to=None, 
                 parent_link=False, to_field=None, db_constraint=True, null=True, blank=True,**kwargs):
        super().__init__(to, on_delete, related_name, related_query_name, 
                         limit_choices_to, parent_link, to_field, db_constraint, verbose_name=verbose_name, null=null, blank=blank, **kwargs)
