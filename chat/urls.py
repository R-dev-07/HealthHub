from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views
from . import consumers

app_name = 'chat'

router = DefaultRouter()
router.register(r'chat-rooms', views.ChatRoomViewSet, basename='chatroom')
router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('list/', views.chat_list, name='chat_list'),
    path('start/<int:doctor_id>/', views.start_chat, name='start_chat'),
    path('<int:chat_room_id>/', views.chat_detail, name='chat_detail'),
    path('<int:chat_room_id>/delete/', views.delete_chat, name='delete_chat'),
]

# WebSocket routing
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
