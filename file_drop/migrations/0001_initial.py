# Generated by Django 4.2.11 on 2024-07-13 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import file_drop.models
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileDrop',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.FileField(storage=file_drop.models.S3MediaStorage(), upload_to='uploads/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
