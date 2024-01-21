from django.shortcuts import render
from .serializers import CalendarTaskSerializer, InboxTaskSerializer, DeletedTaskSerializer, TaskSerializer, RepeatTaskSerializer
from .models import CalendarTask, InboxTask, DeletedTask, Task
from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response
from datetime import timedelta, datetime

class TaskView(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
               
    serializer_class = TaskSerializer
    model_class = Task

    def get_queryset(self):
        user_id = int(self.kwargs['user_id'])
        return self.model_class.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = int(self.kwargs['user_id'])
        serializer.save(user_id=user_id)

    class Meta:
        abstract = True


class CalendarInboxTaskView(TaskView,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):

    
    class Meta:
        abstract = True


class CalendarTaskView(CalendarInboxTaskView):
    serializer_class = CalendarTaskSerializer
    model_class = CalendarTask


class InboxTaskView(CalendarInboxTaskView):
    serializer_class = InboxTaskSerializer
    model_class = InboxTask


class DeletedTaskView(TaskView,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    serializer_class = DeletedTaskSerializer
    model_class = DeletedTask



class RepeatTaskView(generics.CreateAPIView):
    def post(self, request, user_id):
        request.data.update({'user': user_id})
        serializer = RepeatTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            task_id = serializer['task_id'].value
            task = CalendarTask.objects.filter(id=task_id).first()

            every = serializer['every'].value

            task_date = task.date

            task_date += timedelta(days=every)

            repetitions = []

            until = datetime.strptime(serializer['until'].value, "%Y-%m-%d").date()

            while task_date <= until:
                repeated_task = CalendarTask.objects.create(title=task.title, description=task.description, priority=task.priority, date=task_date, user_id=task.user_id)
                repetitions.append(repeated_task.id)
                task_date += timedelta(days=every)
            
            return Response(repetitions, status=status.HTTP_201_CREATED, content_type="application/json")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)