# Generated by Django 3.1.7 on 2021-04-17 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Li_Poster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('word', models.CharField(max_length=255)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Li_Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job_index', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('post_date', models.DateTimeField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Li_jobs', to='project_solo_app.job')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Li_Jobs', to='project_solo_app.li_poster')),
            ],
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('definition', models.TextField()),
                ('source_url', models.CharField(max_length=255)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='definitions', to='project_solo_app.word')),
            ],
        ),
    ]
