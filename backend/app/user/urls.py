from django.urls import path ,include
from .views import MosqueStuffViewSet, PasswordSetView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("mosque-staff",MosqueStuffViewSet,basename="mosque-staff")

urlpatterns = [
    path("",include(router.urls)),
    path("token/",TokenObtainPairView.as_view()),
    path('password-set/<int:uid>/<str:token>/', PasswordSetView.as_view({'post': 'create'}), name='password-set'),
]