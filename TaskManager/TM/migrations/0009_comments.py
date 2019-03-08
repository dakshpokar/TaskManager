# Generated by Django 2.1 on 2019-03-07 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TM', '0008_task_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_generated', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TM.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]