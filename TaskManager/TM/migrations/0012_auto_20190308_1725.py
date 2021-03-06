# Generated by Django 2.1 on 2019-03-08 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TM', '0011_auto_20190308_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TM.UserProfile'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TM.UserProfile'),
        ),
        migrations.AlterField(
            model_name='membershiptotask',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TM.UserProfile'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_members',
            field=models.ManyToManyField(related_name='memberOfTask', through='TM.MembershipToTask', to='TM.UserProfile'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TM.UserProfile'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='members',
            field=models.ManyToManyField(related_name='member', through='TM.Membership', to='TM.UserProfile'),
        ),
    ]
