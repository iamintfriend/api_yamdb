# Generated by Django 2.2.16 on 2022-09-10 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220908_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'пользователь'), ('moderator', 'модератор'), ('admin', 'администратор')], default='user', max_length=10, verbose_name='Роль'),
        ),
    ]
