from django.contrib import admin
from django.urls import path,include
from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    def get(self, request):
        return Response({'test': 'test'})

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('def/',TestView.as_view()),
    path('',include('user.urls')),
]
