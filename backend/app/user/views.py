from rest_framework.generics import CreateAPIView
from .serializers import CustomUserSerializer
from core.models import CustomUser


class CustomUserCreateView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



