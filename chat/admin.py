from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'is_active', 'last_message_at', 'created_at')
    list_filter = ('is_active', 'created_at', 'last_message_at')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name')
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'get_chat_room', 'message_type', 'is_read', 'created_at')
    list_filter = ('message_type', 'is_read', 'created_at')
    search_fields = ('sender__first_name', 'content', 'chat_room__patient__user__first_name')
    
    def get_chat_room(self, obj):
        return str(obj.chat_room)
    get_chat_room.short_description = 'Chat Room'
