from django.db import models
from rest_framework import serializers

from medical_peek_api.model.dmo.medical_resource import MedicalResource, MedicalResourceSerializer


class MedicalItem(models.Model):
    id = models.AutoField(auto_created = True, default = None, primary_key = True)
    nomenclature = models.CharField(max_length = 4096, null = True, blank = True)
    description = models.TextField(null = True)
    nsn = models.IntegerField(max_length = 13, null = True)
    msn = models.CharField(max_length = 1024)
    medical_resource = models.ForeignKey(
        MedicalResource,
        on_delete = models.DO_NOTHING,
        serialize = True,
        primary_key = False,
        null = True,
        blank = True,
        unique = False
    )

    class Meta:
        db_table = 'medical_item'


class MedicalItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null = True, required = False)
    nomenclature = serializers.CharField(allow_null = True, allow_blank = True)
    description = serializers.CharField(allow_null = True, allow_blank = True),
    nsn = serializers.IntegerField(allow_null = True)
    msn = serializers.IntegerField(allow_null = True)
    medical_resource = MedicalResourceSerializer(allow_null = True, read_only = False)

    class Meta:
        model = MedicalItem
        fields = (
            'model',
            'fields',
            'id',
            'nomenclature',
            'description',
            'nsn',
            'msn',
            'medical_resource',
        )
