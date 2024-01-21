from rest_framework import serializers
from .models import CalendarTask, InboxTask, DeletedTask
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'description', 'priority', 'completed', 'user_id')
        abstract = True

class CalendarTaskSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        model = CalendarTask
        fields = TaskSerializer.Meta.fields + ('date',)

class InboxTaskSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        model = InboxTask

class DeletedTaskSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ('deletion_date',)
        model = DeletedTask


class RepeatTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    every = serializers.IntegerField()
    until = serializers.DateField()
    user = serializers.IntegerField()


    def create(self, validated_data):
        if validated_data['user'] == CalendarTask.objects.filter(id=validated_data['task_id']).first().user_id:
            return validated_data
        raise serializers.ValidationError("Task not found")
        

    def validate_task_id(self, task_id):
        calendar_task = CalendarTask.objects.filter(id=task_id)
        if not calendar_task: 
            raise serializers.ValidationError("Task not found")
        return task_id


    def validate_until(self, until):
        if date.today() > until:
            raise serializers.ValidationError("The date must be a day after today")
        return until
        

    def validate_every(self, every):
        if every <= 0:
            raise serializers.ValidationError("The number must be greater than 0")
        return every