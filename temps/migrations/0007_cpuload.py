# Generated by Django 3.2 on 2022-09-01 16:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('temps', '0006_auto_20220806_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cpuload',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('value', models.FloatField(default=0)),
                ('service_equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='temps.serviceequipment')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
