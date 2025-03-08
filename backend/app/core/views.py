from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView,UpdateAPIView
from .serializers import * 
from rest_framework.response import Response
from rest_framework.status import *
from .models import *
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OPENAPI_TYPE_MAPPING
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import NotFound as Http404
from rest_framework import status


class RessourceTypeView (ModelViewSet):
    """CRUD operation about the ressource type"""

    queryset = RessourceType.objects.all()
    serializer_class = RessourceTypeSerialzer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='start_date',
            description='Filter distributions created after this date (format: YYYY-MM-DD)',
            required=False,
            type=str,
            location=OpenApiParameter.QUERY
        )
    ]
)       


class DistributionView (ModelViewSet):

    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        """return the distributions of the user's mosque"""
        distributions = Distribution.objects.filter(responsible__mosque=self.request.user.mosque)

        start_date = self.request.query_params.get('start_date')
        if start_date:
            #filter the distributions that are created after the start_date
            distributions = distributions.filter(start_time__gte=start_date)

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



from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from django.http import Http404

class UploadNeedyDocumentView(UpdateAPIView):
    serializer_class = UploadNeedyDocumentSerializer

    def get_queryset(self):
        """Filter the needys that belong to the responsible user"""
        return Needy.objects.filter(responsible=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get("pk")
        try:
            return queryset.get(id=pk)
        except Needy.DoesNotExist:
            raise Http404("Needy not found")

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        print("Instance before update:", instance)
        print("Request data:", request.data)
        print("Request files:", request.FILES)

        # Combine request.data and request.FILES for file uploads
        data = request.data.copy()
        data.update(request.FILES)

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("Instance after update:", instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class NumberOfResponsiblesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        mosque = request.user.mosque  # Assuming the user has a foreign key to Mosque
        count = CustomUser.objects.filter(mosque=mosque).count()
        return Response({'number_of_responsibles': count}, status=200)
    


class NumberOfNeedyView(APIView):
    """Return the number of needy that belong the same month"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        mosque = request.user.mosque  # Assuming the user has a foreign key to Mosque
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        count = Needy.objects.filter(responsible__mosque=mosque, created_at__gte=start_of_month).count()
        return Response({'number_of_needy': count}, status=200)



# class RessourceViewSet(ModelViewSet):
#     serializer_class = RessourceSerializer
#     queryset = Ressource.objects.all()
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]


#     def get_queryset(self):
#         """Return the ressources of the user's mosque"""
#         return Ressource.objects.filter(distribution__responsible__mosque=self.request.user.mosque)
