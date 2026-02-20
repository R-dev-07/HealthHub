from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'hospitals', views.HospitalViewSet, basename='hospital')
router.register(r'departments', views.DepartmentViewSet, basename='department')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('list/', views.hospital_list, name='hospital_list'),
    path('<int:hospital_id>/', views.hospital_detail, name='hospital_detail'),
    path('<int:hospital_id>/departments/', views.hospital_departments, name='hospital_departments'),
    path('admin/dashboard/', views.hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('create/', views.create_hospital, name='create_hospital'),
    path('<int:hospital_id>/edit/', views.edit_hospital, name='edit_hospital'),
    path('<int:hospital_id>/create-department/', views.create_department, name='create_department'),
    path('<int:hospital_id>/create-service/', views.create_service, name='create_service'),
]
