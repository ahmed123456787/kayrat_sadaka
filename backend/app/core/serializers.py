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
    ressource_type = RessourceTypeSerialzer()
    class Meta:
        model = Ressource
        exclude = ['distribution']
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        """Update the ressource instance with the validated data."""
        ressource_type_data = validated_data.pop('ressource_type')
        ressource_type, created = RessourceType.objects.get_or_create(**ressource_type_data)

        instance.ressource_type = ressource_type
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class DistributionSerializer(ModelSerializer):
    ressources = RessourceSerializer(many=True)

    class Meta:
        model = Distribution
        fields = ["id", "name", "start_time", "finish_time", "ressources"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        ressources = validated_data.pop('ressources')
        distribution = Distribution.objects.create(**validated_data)

        for ressource in ressources:
            ressource_type_data = ressource.pop('ressource_type')
            ressource_type_name = ressource_type_data.get('name')

            # Use get_or_create to handle existing and new RessourceType
            ressource_type, created = RessourceType.objects.get_or_create(name=ressource_type_name)

            # Create Ressource linked to Distribution and RessourceType
            Ressource.objects.create(
                distribution=distribution,
                ressource_type=ressource_type,
                **ressource
            )

        #  Reload the distribution with nested ressources and ressource_type details
        distribution.refresh_from_db()
        return self.to_representation(distribution)



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document 
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class NeedySerializer (ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Needy
        exclude = ['responsible']
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
    



class UploadNeedyDocumentSerializer(serializers.ModelSerializer):
    documents = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Needy
        fields = ['id', 'documents']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        print("Inside custom update method")
        
        # Extract files data if provided
        files = validated_data.pop('documents', [])
        print("Files data:", files)

        # Update the Needy instance
        instance = super().update(instance, validated_data)
        print("Needy instance updated:", instance)

        # Save new documents if provided
        for file in files:
            print("Processing file:", file)
            document = Document.objects.create(file=file)
            instance.documents.add(document)

        instance.save()
        return instance


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