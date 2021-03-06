# Generated by Django 2.1 on 2018-08-05 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='User name')),
                ('uri', models.URLField(unique=True, verbose_name='User URI')),
            ],
            options={
                'verbose_name': 'Reddit Author',
                'verbose_name_plural': 'Reddit Authors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('label', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='Label')),
                ('term', models.CharField(max_length=25, verbose_name='Term')),
            ],
            options={
                'verbose_name': 'Reddit Category',
                'verbose_name_plural': 'Reddit Categories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('updated_at', models.DateTimeField(verbose_name='Updated at')),
                ('id', models.CharField(max_length=9, primary_key=True, serialize=False, verbose_name='reddit id')),
                ('link', models.URLField(max_length=300, verbose_name='URL')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='target_reddit.Author', verbose_name='Post author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='target_reddit.Category', verbose_name='Post category')),
            ],
            options={
                'verbose_name': 'Reddit Post',
                'verbose_name_plural': 'Reddit Posts',
                'managed': True,
            },
        ),
    ]
