from .serializers import StaffSerializer
from rest_framework.viewsets import ModelViewSet
from .permission import IsMosqueAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin,DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model



class MosqueStuffViewSet(GenericViewSet,CreateModelMixin,
                        ListModelMixin,DestroyModelMixin):
    
    """Create a new staff for the mosque by the admin"""
    serializer_class = StaffSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsMosqueAdmin,IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """Filter the staff by the mosque"""
        return self.queryset.filter(mosque=self.request.user.mosque)

    def create(self, request, *args, **kwargs):
        
        serailizer = self.get_serializer(data=request.data)
        if serailizer.is_valid(raise_exception=True):
            serailizer.save(mosque=request.user.mosque) # Assign the mosque to the staff
            return Response(serailizer.data, status=status.HTTP_201_CREATED)    
        else:
            return Response(serailizer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
















#  class CustomUserCreateView(CreateAPIView):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()

#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)