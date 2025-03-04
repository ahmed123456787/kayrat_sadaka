from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import  serializers
from .models import *

class RessourceTypeSerialzer (ModelSerializer):
    """Serializer of the ressource type"""
    class Meta:
        model = RessourceType
        fields = "__all__"

class RessourceSerializer(ModelSerializer):
    """Serializer of the ressource"""
    class Meta:
        model = Ressource
        fields = "__all__"
        read_only_fields = ["id"]


class DistributionSerializer(ModelSerializer):
    class Meta: 
        model = Distribution
        fields = ["id","name"]  
        read_only_fields = ["id"]


class NeedySerializer (ModelSerializer):
    class Meta:
        model = Needy
        fields = ['id','first_name','last_name','phone_number','address','birth_date','created_at'] 
        read_only_fields = ['id']

    def validate_phone_number(self, value):
        """Ensure the phone number starts with '0' and has exactly 10 digits."""
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if not value.startswith("0"):
            raise serializers.ValidationError("Phone number must start with 0.")
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits long.")
        return value 
    


class UploadNeedyDocumentSerailizer(Serializer):
    documents = serializers.JSONField()



class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','content','user','read']
        read_only_fields = ['id']



class NumberOfResponsiblesView(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','email']
        read_only_fields = ['id']