from django.db import models
from django.db.models import QuerySet
from patients.models import Patient, CustomUser


class ChatRoom(models.Model):
    """Chat room for conversations between doctor and patient"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chat_rooms')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='chat_rooms')
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='chat_room')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Chat Rooms'
        unique_together = ('patient', 'doctor')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat: {self.patient.user.get_full_name()} & Dr. {self.doctor.user.get_full_name()}"

    def get_last_message(self) -> 'Message | None':
        """Get last message in this room"""
        return self.messages.all().order_by('-created_at').first()


class Message(models.Model):
    """Chat messages"""
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('prescription', 'Prescription'),
    ]
    
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField()
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Messages'
        ordering = ['created_at']

    def __str__(self):
        return f"Message by {self.sender.get_full_name()} in {self.chat_room}"
