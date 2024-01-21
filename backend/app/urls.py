from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app import views

app_name = 'app'

router = routers.DefaultRouter()
router.register(r'(?P<user_id>\d+)/calendar', views.CalendarTaskView, 'calendar')
router.register(r'(?P<user_id>\d+)/inbox', views.InboxTaskView, 'inbox')
router.register(r'(?P<user_id>\d+)/trash', views.DeletedTaskView, 'trash')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:user_id>/repeat', views.RepeatTaskView.as_view(), name="repeat"),
]