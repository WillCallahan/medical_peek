from django.db import models
from rest_framework import serializers


class FileExtractor(models.Model):
    id = models.AutoField(auto_created = True, default = None, primary_key = True)
    file = models.FileField(null = False, blank = False, upload_to = 'files/%Y/%m/%d/')
    title = models.CharField(null = False, blank = False, max_length = 1024)
    group_uuid = models.UUIDField(null = False, blank = False)
    description = models.TextField(null = True, blank = True, max_length = 4096)
    mime_type = models.CharField(null = False, blank = False, default = 'text/plain', max_length = 50)
    file_name = models.CharField(null = False, blank = False, default = 'unnamed_file', max_length = 255)

    class Meta:
        db_table = 'file_extractor'


class FileExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtractor
        fields = (
            'id',
            'title',
            'group_uuid',
            'description',
            'mime_type',
            'file_name',
        )
