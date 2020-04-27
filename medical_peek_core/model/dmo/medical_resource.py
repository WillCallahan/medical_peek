from django.db import models
from rest_framework import serializers


class MedicalResource(models.Model):
    id = models.AutoField(auto_created = True, default = None, primary_key = True)
    description = models.TextField(null = True)
    content = models.TextField(null = True)
    link = models.CharField(max_length = 4096, null = True)

    class Meta:
        db_table = 'medical_resource'


class MedicalResourceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null = True, required = False)
    description = serializers.CharField(allow_null = True, allow_blank = True),
    content = serializers.CharField(allow_null = True, allow_blank = True),
    link = serializers.CharField(allow_null = True, allow_blank = True, max_length = 4096)

    class Meta:
        model = MedicalResource
        fields = (
            'id',
            'description',
            'content',
            'link'
        )
