from django.urls import path ,include
from .views import MosqueStuffViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("mosque-staff",MosqueStuffViewSet,basename="mosque-staff")

urlpatterns = [
    path("",include(router.urls)),
    path("token/",TokenObtainPairView.as_view())
]