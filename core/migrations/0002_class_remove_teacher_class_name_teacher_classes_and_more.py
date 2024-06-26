# Generated by Django 5.0.6 on 2024-06-12 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='class_name',
        ),
        migrations.AddField(
            model_name='teacher',
            name='classes',
            field=models.ManyToManyField(to='core.class'),
        ),
        migrations.AlterField(
            model_name='student',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.class'),
        ),
    ]
