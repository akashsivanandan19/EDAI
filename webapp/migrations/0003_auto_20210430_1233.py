# Generated by Django 3.1.7 on 2021-04-30 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(default=32, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('A', 'Assigned'), ('W', 'Waiting'), ('P', 'In Progress'), ('C', 'Completed')], default='A', max_length=1),
        ),
    ]
