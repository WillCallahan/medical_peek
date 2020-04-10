# Generated by Django 3.0.5 on 2020-04-10 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalResource',
            fields=[
                ('id', models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False)),
                ('description', models.TextField(null=True)),
                ('link', models.CharField(max_length=4096, null=True)),
            ],
            options={
                'db_table': 'medical_resource',
            },
        ),
        migrations.CreateModel(
            name='MedicalItem',
            fields=[
                ('id', models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False)),
                ('nomenclature', models.CharField(blank=True, max_length=4096, null=True)),
                ('description', models.TextField(null=True)),
                ('nsn', models.IntegerField(max_length=13, null=True)),
                ('msn', models.CharField(max_length=1024)),
                ('medical_resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='medical_peek.MedicalResource')),
            ],
            options={
                'db_table': 'medical_item',
            },
        ),
    ]
