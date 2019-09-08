from django.conf.urls import url
from django.contrib import admin
from django.urls import path , include
from . import views
from rest_framework import routers
from chat.views import *
from django.contrib.auth.views import LogoutView
router = routers.DefaultRouter()

# router.register(r'message-detail', views.message_list)

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),

    path('logout', LogoutView.as_view(next_page='index'), name='logout'),
    #{'next_page': 'index'} is specified to redirect the User after logging out.
    url(r'^chat/',views.chat_view, name='chats'),
    # path('chats', views.chat_view, name='chats'),
    # URL form : "/api/messages/1/2"
     path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),  # For GET request.
    # URL form : "/api/messages/"
    path('api/messages', views.message_list, name='message-list'),   # For POST
    # URL form "/api/users/1"
    # path('api/users/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    path('api/users/', views.user_list, name='user-list'),    # POST for new user and GET for all users list
]