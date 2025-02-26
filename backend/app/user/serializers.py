from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


class StaffSerializer(ModelSerializer):
    """Serializer for the stuff object"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserSerializer(ModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'email','password']
        read_only_fields = ['id']  
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}      