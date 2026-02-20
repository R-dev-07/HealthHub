from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='user')
router.register(r'patients', views.PatientViewSet, basename='patient')
router.register(r'reviews', views.PatientReviewViewSet, basename='review')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
    path('reports/', views.patient_reports, name='patient_reports'),
    path('appointments/', views.patient_appointments, name='patient_appointments'),
    path('search-hospitals/', views.search_hospitals, name='search_hospitals'),
    path('search-doctors/', views.search_doctors, name='search_doctors'),
    path('write-review/<int:doctor_id>/', views.write_review, name='write_review'),
]
