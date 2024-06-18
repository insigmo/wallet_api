from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

router = DefaultRouter()
router.register('wallet', views.WalletViewSet, basename='wallet')
router.register('transaction', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]
