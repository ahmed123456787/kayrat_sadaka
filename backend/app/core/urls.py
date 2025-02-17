from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ressources-type', RessourceTypeView, basename='ressources-type')
router.register('distributions', DistributionView, basename='distributions')

urlpatterns = [
    path('needy/<int:pk>/', UploadNeedyDocumentView.as_view(), name='upload_needy_document'),
    path('needy/', NeedyView.as_view(), name='needy'),
    path('', include(router.urls)),
]