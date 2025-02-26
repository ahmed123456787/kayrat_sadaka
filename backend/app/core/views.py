from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView,UpdateAPIView
from .serializers import * 
from rest_framework.response import Response
from rest_framework.status import *
from .models import *



class RessourceTypeView (ModelViewSet):
    """CRUD operation about the ressource type"""

    queryset = RessourceType.objects.all()
    serializer_class = RessourceTypeSerialzer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
        
class DistributionView (ModelViewSet):

    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        """return the distributions of the user's mosque"""
        distributions = Distribution.objects.filter(responsible__mosque=self.request.user.mosque)
        return distributions

    def create(self, request, *args, **kwargs):

        serializer = DistributionSerializer(data=request.data)

        if serializer.is_valid():
            responsible = self.request.user
            
            serializer.save(responsible=responsible)
            return Response(serializer.validated_data,status=HTTP_201_CREATED)
        
        else :
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
        


class NeedyView(ListCreateAPIView):

    serializer_class = NeedySerializer
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        """Retrieve the needy that belong to the logged-in user's mosque"""
        user = self.request.user  
        if user.mosque:  # Ensure the user is associated with a mosque
            return Needy.objects.filter(responsible__mosque=user.mosque)
        return Needy.objects.none() 


    def create(self, request, *args, **kwargs):
        serializer = NeedySerializer(data=request.data)
        if serializer.is_valid():
            responsible = self.request.user
            serializer.save(responsible=responsible)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



class UploadNeedyDocumentView(UpdateAPIView):
    serializer_class = UploadNeedyDocumentSerailizer


    def get_queryset(self):
        """Filter the needys that belongs the responsible mosque """
    def partial_update(self, request, *args, **kwargs):

        serializer = UploadNeedyDocumentSerailizer(data=request.data)

        if serializer.is_valid():
            serializer

        return super().partial_update(request, *args, **kwargs)   



class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        """return the queryset"""