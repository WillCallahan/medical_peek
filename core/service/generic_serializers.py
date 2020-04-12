import importlib
import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)


class RecursiveField(serializers.Serializer):
    """
    Support the ability to have recursive serializers
    """

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context = self.context)
        return serializer.data

    def to_internal_value(self, data):
        serializer = self.parent.parent.__class__(data = data)
        serializer.is_valid()
        return serializer.validated_data


class ModuleSerializerField(serializers.Serializer):
    """
    Provides the ability to use a Serializer based on the module name that
    the serializer is packages in and the name of the class of the serializer.
    """

    def create(self, validated_data):
        serializer_instance = getattr(importlib.import_module(self.module_name), self.class_name)()
        return serializer_instance.create(validated_data)

    def update(self, instance, validated_data):
        serializer_instance = getattr(importlib.import_module(self.module_name), self.class_name)()
        return serializer_instance.update(instance, validated_data)

    def to_representation(self, value):
        serializer = getattr(importlib.import_module(self.module_name), self.class_name)(value)
        return serializer.data

    def to_internal_value(self, data):
        serializer = getattr(importlib.import_module(self.module_name), self.class_name)(data = data)
        serializer.is_valid()
        return serializer.validated_data

    def __init__(self, module_name, class_name, **kwargs):
        """

        :param module_name: Name of the module containing the serializer
        :type module_name: str
        :param class_name: Name of the serializer class
        :type class_name: str
        :param kwargs:
        :type kwargs:
        """
        super(ModuleSerializerField, self).__init__(**kwargs)
        self.module_name = module_name
        self.class_name = class_name


class ListOrDictField(serializers.Serializer):
    """
    Determines whether to use a ListSerializer or DictSerializer based on the data provided
    """

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def to_representation(self, data):
        if isinstance(data, list):
            serializer = serializers.ListField(required = self.required, allow_null = self.allow_null)
        elif isinstance(data, dict):
            serializer = serializers.DictField(required = self.required, allow_null = self.allow_null)
        else:
            logger.warn("ListOrDictField data does not match a list or dict")
            serializer = serializers.CharField(required = self.required, allow_null = self.allow_null)
        return serializer.to_representation(data)

    def to_internal_value(self, data):
        if isinstance(data, tuple):
            data = list(data)
            serializer = serializers.ListField(required = self.required, allow_null = self.allow_null)
        elif isinstance(data, list):
            serializer = serializers.ListField(required = self.required, allow_null = self.allow_null)
        elif isinstance(data, dict):
            serializer = serializers.DictField(required = self.required, allow_null = self.allow_null)
        else:
            logger.warn("ListOrDictField data does not match a list or dict")
            serializer = serializers.CharField(required = self.required, allow_null = self.allow_null)
        return serializer.to_internal_value(data)
