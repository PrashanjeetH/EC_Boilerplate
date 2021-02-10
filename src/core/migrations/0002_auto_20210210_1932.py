# Generated by Django 3.1.6 on 2021-02-10 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirts'), ('TS', 'T-Shirts'), ('OW', 'Out Sports')], default='S', max_length=2),
        ),
        migrations.AddField(
            model_name='item',
            name='labels',
            field=models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], default='P', max_length=1),
        ),
    ]
