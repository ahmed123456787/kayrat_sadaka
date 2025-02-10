from django.urls import path 
from .views import CustomUserCreateView

urlpatterns = [
    path("users/", CustomUserCreateView.as_view(), name="user-list"),
]