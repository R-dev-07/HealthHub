from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from .forms import MessageForm
from doctors.models import Doctor
from patients.models import Patient


# API Views
class ChatRoomViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Chat Rooms"""
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            return ChatRoom.objects.filter(patient=user.patient_profile)
        elif hasattr(user, 'doctor_profile'):
            return ChatRoom.objects.filter(doctor=user.doctor_profile)
        return ChatRoom.objects.none()
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a chat room"""
        chat_room = self.get_object()
        messages = chat_room.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """API ViewSet for Messages"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            return Message.objects.filter(chat_room__patient=user.patient_profile)
        elif hasattr(user, 'doctor_profile'):
            return Message.objects.filter(chat_room__doctor=user.doctor_profile)
        return Message.objects.none()


# Function-based Views
@login_required
def chat_list(request):
    """List all chat rooms for the user"""
    if hasattr(request.user, 'patient_profile'):
        chat_rooms = ChatRoom.objects.filter(patient=request.user.patient_profile).order_by('-last_message_at')
    elif hasattr(request.user, 'doctor_profile'):
        chat_rooms = ChatRoom.objects.filter(doctor=request.user.doctor_profile).order_by('-last_message_at')
    else:
        chat_rooms = ChatRoom.objects.none()
    
    context = {'chat_rooms': chat_rooms}
    return render(request, 'chat/list.html', context)


@login_required
def start_chat(request, doctor_id):
    """Start a new chat with a doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patient = get_object_or_404(Patient, user=request.user)
    
    chat_room, created = ChatRoom.objects.get_or_create(
        patient=patient,
        doctor=doctor
    )
    
    return redirect('chat:chat_detail', chat_room_id=chat_room.id)


@login_required
def chat_detail(request, chat_room_id):
    """Chat detail view"""
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    
    # Check if user has access
    if hasattr(request.user, 'patient_profile'):
        if chat_room.patient.user != request.user:
            return redirect('chat:chat_list')
    elif hasattr(request.user, 'doctor_profile'):
        if chat_room.doctor.user != request.user:
            return redirect('chat:chat_list')
    else:
        return redirect('home')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_room = chat_room
            message.sender = request.user
            message.save()
            
            chat_room.last_message_at = timezone.now()
            chat_room.save()
            
            return redirect('chat:chat_detail', chat_room_id=chat_room.id)
    else:
        form = MessageForm()
    
    messages = chat_room.messages.all().order_by('created_at')
    
    # Mark messages as read
    unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
    for message in unread_messages:
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
    
    context = {
        'chat_room': chat_room,
        'messages': messages,
        'form': form,
    }
    return render(request, 'chat/detail.html', context)


@login_required
def delete_chat(request, chat_room_id):
    """Delete a chat room"""
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    
    # Check access
    if hasattr(request.user, 'patient_profile'):
        if chat_room.patient.user != request.user:
            return redirect('chat:chat_list')
    elif hasattr(request.user, 'doctor_profile'):
        if chat_room.doctor.user != request.user:
            return redirect('chat:chat_list')
    else:
        return redirect('home')
    
    if request.method == 'POST':
        chat_room.delete()
        return redirect('chat:chat_list')
    
    context = {'chat_room': chat_room}
    return render(request, 'chat/confirm_delete.html', context)
