from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerPage, name = 'register'),
    
    path('', views.home, name = 'home'),
    path('room/<int:pk>/', views.room, name = 'room'),
    path('profile/<int:pk>', views.userProfile, name='user-profile'),
    
    path('create-room/', views.createRoom, name = 'create-room'),
    path('update-room/<int:pk>/', views.updateRoom, name = 'update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name = 'delete-room'),
    path('delete-message/<int:pk>/', views.deleteMessage, name = 'delete-message'),
    path('join-room/<int:pk>/', views.joinRoom, name = 'join-room'),
    path('leave-room/<int:pk>/', views.leaveRoom, name = 'leave-room'),
    
    path('update_user/', views.updateUser, name='update-user'),
    
    path('topics/', views.topicsPage, name='topics'),
    path('activities/', views.activityPage, name='activities'),
]