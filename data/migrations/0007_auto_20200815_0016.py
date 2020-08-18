# Generated by Django 3.0.8 on 2020-08-15 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20200814_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appstorereview',
            name='author',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='appstorereview',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='appstorereview',
            name='country',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.DeleteModel(
            name='PlayStoreReview',
        ),
    ]
