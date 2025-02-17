from rest_framework.serializers import ModelSerializer
from core.models import CustomUser
from django.contrib.auth import get_user_model



# class CustomUserSerializer(ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'email','password', 'first_name', 'last_name', 'mosque']
#         extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
#     def create(self, validated_data):
#        """Create a new user with encrypted password and return it"""
#        return get_user_model().objects.create_user(**validated_data)




class StaffSerializer(ModelSerializer):
    """Serializer for the stuff object"""
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']