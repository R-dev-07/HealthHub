from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'appointments'

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('book/<int:doctor_id>/', views.book_appointment, name='book'),
    path('<int:appointment_id>/', views.appointment_detail, name='detail'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('doctor-appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve'),
    path('reject/<int:appointment_id>/', views.reject_appointment, name='reject'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel'),
]
