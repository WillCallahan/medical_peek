from django.db import models
from rest_framework import serializers


class BasicFile(models.Model):
    id = models.AutoField(auto_created = True, default = None, primary_key = True)
    file = models.FileField(null = False, blank = False, upload_to = 'files/%Y/%m/%d/')
    mime_type = models.CharField(null = False, blank = False, default = 'text/plain', max_length = 50)
    file_name = models.CharField(null = False, blank = False, default = 'unnamed_file', max_length = 255)
    category = models.SmallIntegerField(null = False, blank = False)

    class Meta:
        db_table = 'basic_file'


class BasicFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicFile
        fields = (
            'id',
            'mime_type',
            'file_name',
            'category',
        )
