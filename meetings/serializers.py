from rest_framework import serializers
from .models import Object, Visit
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ['id', 'name']


class VisitSerializer(serializers.ModelSerializer):
    visiter = UserSerializer(read_only=True)
    objct = ObjectSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = [
            'id', 'visiter', 'objct', 'is_started', 'date', 'started', 'ended'
        ]


class VisitCreateSerializer(serializers.ModelSerializer):
    visiter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    objct = serializers.PrimaryKeyRelatedField(queryset=Object.objects.all())

    class Meta:
        model = Visit
        fields = ['visiter', 'objct', 'date']

    def create(self, validated_data):
        return Visit.objects.create(**validated_data)


class ReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    all_visits = serializers.ListField(child=serializers.DictField())
    ended_visits = serializers.ListField(child=serializers.DictField())
    planed_visits = serializers.ListField(child=serializers.DictField())
    len_of_user_objects = serializers.IntegerField()
    objects_count = serializers.DictField()
    unic_objects_visited_by_user = serializers.ListField(
        child=serializers.DictField()
    )
