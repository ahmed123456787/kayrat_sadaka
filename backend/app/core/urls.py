from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ressources-type', RessourceTypeView, basename='ressources-type')
router.register('distributions', DistributionView, basename='distributions')
router.register('ressources', RessourceViewSet, basename='ressources')

urlpatterns = [
    path('needy/<int:pk>/', UploadNeedyDocumentView.as_view(), name='upload_needy_document'),
    path('needy/', NeedyView.as_view(), name='needy'),
    path('number-of-responsibles/', NumberOfResponsiblesView.as_view(), name='number_of_responsibles'),
    path('number-of-needy/', NumberOfNeedyView.as_view(), name='number_of_needy'),
    path('', include(router.urls)),

]