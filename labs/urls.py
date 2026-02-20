from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'labs'

router = DefaultRouter()
router.register(r'tests', views.LabTestViewSet, basename='test')
router.register(r'reports', views.LabReportViewSet, basename='report')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('tests/', views.lab_tests, name='tests'),
    path('select-tests/', views.select_lab_tests, name='select_tests'),
    path('my-orders/', views.patient_lab_orders, name='my_orders'),
    path('my-reports/', views.patient_lab_reports, name='my_reports'),
    path('worker-dashboard/', views.lab_worker_dashboard, name='worker_dashboard'),
    path('upload-report/<int:order_id>/', views.upload_lab_report, name='upload_report'),
]
