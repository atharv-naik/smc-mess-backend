# Generated by Django 4.1 on 2023-06-17 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smc', '0003_alter_student_account_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='qty',
            field=models.IntegerField(default=200),
        ),
    ]
