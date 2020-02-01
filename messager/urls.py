from django.urls import path
from messager import views
app_name = 'messager'

urlpatterns = [
  path('', views.MessagesListView.as_view(), name="messages_list"),
  path('<username>/', views.ConversationListView.as_view(), name="conversation_detail"),
]