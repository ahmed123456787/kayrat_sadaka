from .serializers import StaffSerializer, UserSerializer
from .permission import IsMosqueAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin,DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ObjectDoesNotExist


from .services.email import send_password_reset_email


class MosqueStuffViewSet(GenericViewSet,CreateModelMixin,
                        ListModelMixin,DestroyModelMixin):
    
    """Create a new staff for the mosque by the admin"""
    serializer_class = StaffSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsMosqueAdmin,IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """Filter the staff by the mosque"""

        return self.queryset.filter(mosque=self.request.user.mosque).exclude(email=self.request.user.email)

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(mosque=request.user.mosque,is_active=False) # Assign the mosque to the staff
            user = get_user_model().objects.get(id=serializer.instance.id)
            send_password_reset_email(user) # Pass the user instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordSetView(CreateModelMixin, GenericViewSet):
    """Set the password for the staff after receiving the email"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def verify_password_reset_token(self, uid, token):
        UserModel = get_user_model()
        try:
            print(f"Raw UID from URL: {uid}")  # Debug UID
            try:
                uid = int(uid)
                print(f"Converted UID to integer: {uid}")
            except ValueError:
                print(f"Error: UID '{uid}' is not a valid integer.")
                return None

            try:
                user = UserModel.objects.get(pk=uid)
                print(f"User found: {user}")
            except ObjectDoesNotExist:
                print(f"User with ID {uid} does not exist.")
                return None

            if token_generator.check_token(user, token):
                print("Token is valid")
                return user
            else:
                print("Token is invalid")
        except Exception as e:
            print(f"Error: {e}")  # Debugging errors

        return None
 
    def create(self, request, *args, **kwargs):
        uid = kwargs.get('uid')  # This is already a string
        token = kwargs.get('token')  # This is already the token string
        user = self.verify_password_reset_token(uid, token)
        print(f"User after verification: {user}")  # Debugging
        if user is not None:
            serializer = self.get_serializer(user,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                user.is_active = True
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'status': 'password set'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid token or user ID'}, status=status.HTTP_400_BAD_REQUEST)