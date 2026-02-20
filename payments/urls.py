from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'payments'

router = DefaultRouter()
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'refunds', views.RefundRequestViewSet, basename='refund')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('initiate/<str:payment_type>/<int:object_id>/', views.initiate_payment, name='initiate'),
    path('gateway/<int:payment_id>/', views.payment_gateway, name='payment_gateway'),
    path('success/', views.payment_success, name='success'),
    path('failed/', views.payment_failed, name='failed'),
    path('cancelled/', views.payment_cancelled, name='cancelled'),
    path('history/', views.payment_history, name='history'),
    path('refund/<int:payment_id>/', views.request_refund, name='request_refund'),
    path('refund-detail/<int:refund_id>/', views.refund_detail, name='refund_detail'),
]
