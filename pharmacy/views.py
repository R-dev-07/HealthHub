from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Medicine, MedicineOrder, MedicineOrderItem, Pharmacist
from .serializers import MedicineSerializer, MedicineOrderSerializer, PharmacistSerializer
from .forms import MedicineForm, MedicineOrderForm, AddToCartForm
from patients.models import Patient


# API Views
class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Medicines"""
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Medicine.objects.filter(is_available=True)


class MedicineOrderViewSet(viewsets.ModelViewSet):
    """API ViewSet for Medicine Orders"""
    queryset = MedicineOrder.objects.all()
    serializer_class = MedicineOrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            return MedicineOrder.objects.filter(patient=user.patient_profile)
        elif user.role == 'pharmacist':
            return MedicineOrder.objects.all()
        return MedicineOrder.objects.none()


# Function-based Views
def medicine_list(request):
    """List all medicines"""
    medicines = Medicine.objects.filter(is_available=True)
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    
    if category_filter:
        medicines = medicines.filter(category=category_filter)
    
    if search_query:
        medicines = medicines.filter(name__icontains=search_query)
    
    context = {
        'medicines': medicines,
        'category_filter': category_filter,
        'search_query': search_query,
        'categories': Medicine.CATEGORY_CHOICES,
    }
    return render(request, 'pharmacy/medicine_list.html', context)


def medicine_detail(request, medicine_id):
    """Medicine detail view"""
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    context = {'medicine': medicine}
    return render(request, 'pharmacy/medicine_detail.html', context)


@login_required
def add_to_cart(request, medicine_id):
    """Add medicine to cart"""
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    if not request.user.patient_profile:
        return redirect('home')
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            if quantity > medicine.stock_quantity:
                return JsonResponse({'error': 'Not enough stock'}, status=400)
            
            # Get or create cart session
            cart = request.session.get('medicine_cart', {})
            cart[str(medicine_id)] = {
                'name': medicine.name,
                'price': str(medicine.price),
                'quantity': quantity,
            }
            request.session['medicine_cart'] = cart
            
            return redirect('pharmacy:view_cart')
    else:
        form = AddToCartForm()
    
    context = {'form': form, 'medicine': medicine}
    return render(request, 'pharmacy/add_to_cart.html', context)


@login_required
def view_cart(request):
    """View shopping cart"""
    cart = request.session.get('medicine_cart', {})
    total = sum([float(item['price']) * item['quantity'] for item in cart.values()])
    
    context = {
        'cart': cart,
        'total': total,
    }
    return render(request, 'pharmacy/cart.html', context)


@login_required
def remove_from_cart(request, medicine_id):
    """Remove medicine from cart"""
    cart = request.session.get('medicine_cart', {})
    
    if str(medicine_id) in cart:
        del cart[str(medicine_id)]
        request.session['medicine_cart'] = cart
    
    return redirect('pharmacy:view_cart')


@login_required
def checkout(request):
    """Checkout"""
    patient = get_object_or_404(Patient, user=request.user)
    cart = request.session.get('medicine_cart', {})
    
    if not cart:
        return redirect('pharmacy:view_cart')
    
    if request.method == 'POST':
        form = MedicineOrderForm(request.POST)
        if form.is_valid():
            total_amount = sum([float(item['price']) * item['quantity'] for item in cart.values()])
            
            order = MedicineOrder.objects.create(
                patient=patient,
                total_amount=total_amount,
                delivery_address=form.cleaned_data['delivery_address'],
                notes=form.cleaned_data['notes'],
            )
            
            for medicine_id, item in cart.items():
                medicine = get_object_or_404(Medicine, id=int(medicine_id))
                MedicineOrderItem.objects.create(
                    order=order,
                    medicine=medicine,
                    quantity=item['quantity'],
                    unit_price=float(item['price']),
                )
                # Reduce stock
                medicine.stock_quantity -= item['quantity']
                medicine.save()
            
            # Clear cart
            request.session['medicine_cart'] = {}
            
            return redirect('pharmacy:proceed_to_payment', order_id=order.id)
    else:
        form = MedicineOrderForm()
    
    total = sum([float(item['price']) * item['quantity'] for item in cart.values()])
    
    context = {
        'form': form,
        'cart': cart,
        'total': total,
    }
    return render(request, 'pharmacy/checkout.html', context)


@login_required
def patient_orders(request):
    """View patient's medicine orders"""
    patient = get_object_or_404(Patient, user=request.user)
    orders = patient.medicine_orders.all().order_by('-created_at')
    
    context = {'orders': orders}
    return render(request, 'pharmacy/my_orders.html', context)


@login_required
def pharmacist_dashboard(request):
    """Pharmacist dashboard"""
    if request.user.role != 'pharmacist':
        return redirect('home')
    
    medicines = Medicine.objects.all()
    pending_orders = MedicineOrder.objects.filter(status='pending_payment').count()
    delivered_orders = MedicineOrder.objects.filter(status='delivered').count()
    low_stock_medicines = Medicine.objects.filter(stock_quantity__lt=5)
    
    context = {
        'medicines_count': medicines.count(),
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'low_stock_medicines': low_stock_medicines,
    }
    return render(request, 'pharmacy/pharmacist_dashboard.html', context)


@login_required
def manage_medicines(request):
    """Manage medicines (for pharmacists)"""
    if request.user.role != 'pharmacist':
        return redirect('home')
    
    medicines = Medicine.objects.all()
    
    context = {'medicines': medicines}
    return render(request, 'pharmacy/manage_medicines.html', context)


@login_required
def create_medicine(request):
    """Create new medicine (for pharmacists)"""
    if request.user.role != 'pharmacist':
        return redirect('home')
    
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:manage_medicines')
    else:
        form = MedicineForm()
    
    context = {'form': form}
    return render(request, 'pharmacy/create_medicine.html', context)


@login_required
def edit_medicine(request, medicine_id):
    """Edit medicine (for pharmacists)"""
    if request.user.role != 'pharmacist':
        return redirect('home')
    
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:manage_medicines')
    else:
        form = MedicineForm(instance=medicine)
    
    context = {'form': form, 'medicine': medicine}
    return render(request, 'pharmacy/edit_medicine.html', context)
