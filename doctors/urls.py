from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet, basename='doctor')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.doctor_profile_setup, name='doctor_profile'),
    path('hospitals/', views.doctor_hospitals, name='doctor_hospitals'),
    path('register-hospital/<int:hospital_id>/', views.register_hospital, name='register_hospital'),
    path('patients/', views.doctor_patients, name='doctor_patients'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('create-prescription/<int:appointment_id>/', views.create_prescription, name='create_prescription'),
    path('view-prescription/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
]
