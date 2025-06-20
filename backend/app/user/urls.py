from django.urls import path, include
from .views import MosqueStuffViewSet, PasswordSetView, CustomTokenObtainPairView, CustomTokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("mosque-staff", MosqueStuffViewSet, basename="mosque-staff")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view()),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('password-set/<int:uid>/<str:token>/', PasswordSetView.as_view({'post': 'create'}), name='password-set'),
]