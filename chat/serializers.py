from rest_framework import serializers
from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'sender_name', 'message_type', 'content', 'file', 'is_read',
                  'created_at', 'read_at')
        read_only_fields = ('id', 'created_at', 'read_at')


class ChatRoomSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ('id', 'patient_name', 'doctor_name', 'is_active', 'created_at',
                  'last_message_at', 'last_message')
        read_only_fields = ('id', 'created_at')
    
    def get_last_message(self, obj):
        last_msg = obj.get_last_message()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None
