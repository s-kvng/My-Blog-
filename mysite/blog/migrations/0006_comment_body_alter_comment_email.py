# Generated by Django 4.1.3 on 2022-12-05 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_comment_blog_commen_created_0e6ed4_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='body',
            field=models.TextField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
