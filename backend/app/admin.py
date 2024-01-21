from django.contrib import admin
from .models import CalendarTask, InboxTask, DeletedTask

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'description', 'priority', 'completed')

class CalendarTaskAdmin(TaskAdmin):
    list_display = TaskAdmin.list_display + ('date',)

class InboxTaskAdmin(TaskAdmin):
    pass

class DeletedTaskAdmin(TaskAdmin):
    list_display = TaskAdmin.list_display + ('deletion_date',)

# Register your models here.

admin.site.register(CalendarTask, CalendarTaskAdmin)
admin.site.register(InboxTask, InboxTaskAdmin)
admin.site.register(DeletedTask, DeletedTaskAdmin)
