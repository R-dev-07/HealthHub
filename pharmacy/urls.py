from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'pharmacy'

router = DefaultRouter()
router.register(r'medicines', views.MedicineViewSet, basename='medicine')
router.register(r'orders', views.MedicineOrderViewSet, basename='order')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicine/<int:medicine_id>/', views.medicine_detail, name='medicine_detail'),
    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:medicine_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.patient_orders, name='my_orders'),
    path('pharmacist-dashboard/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
    path('manage-medicines/', views.manage_medicines, name='manage_medicines'),
    path('create-medicine/', views.create_medicine, name='create_medicine'),
    path('edit-medicine/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
]
