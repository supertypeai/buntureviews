# Generated by Django 3.0.8 on 2020-07-17 11:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appName', models.CharField(max_length=60)),
                ('store', models.CharField(max_length=30)),
                ('appid', models.CharField(max_length=60)),
                ('publisher', models.CharField(max_length=60)),
                ('category', models.CharField(max_length=30)),
                ('similar', models.ManyToManyField(blank=True, related_name='_app_similar_+', to='data.App')),
            ],
        ),
        migrations.CreateModel(
            name='AppStoreReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=60)),
                ('version', models.CharField(max_length=10)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('content', models.TextField()),
                ('country', models.CharField(max_length=2)),
                ('app', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.App')),
            ],
        ),
        migrations.CreateModel(
            name='PlayStoreReview',
            fields=[
                ('appstorereview_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.AppStoreReview')),
                ('authorImg', models.URLField()),
                ('reviewedAt', models.DateTimeField()),
                ('replyContent', models.TextField()),
                ('repliedAt', models.DateTimeField()),
            ],
            options={
                'ordering': ['-reviewedAt'],
            },
            bases=('data.appstorereview',),
        ),
    ]