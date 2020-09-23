# Generated by Django 3.1.1 on 2020-09-22 21:51

import cmdb.fields
from django.db import migrations, models
import markdownx.models

def default_group(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    ServiceGroup = apps.get_model("cmdb", "ServiceGroup")
    service_group = ServiceGroup()
    service_group.name = "Virtualization"
    service_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', cmdb.fields.StringField(max_length=250, verbose_name='Nome')),
                ('comments', markdownx.models.MarkdownxField(blank=True, null=True, verbose_name='Comments')),

            ],
            options={
                'verbose_name': 'Service group',
                'verbose_name_plural': 'Services groups',
            },
        ),
        migrations.RunPython(default_group),
    ]