from django.db import models
from users.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date


def validate_date(selected_date):
    if selected_date < date.today():
        raise ValidationError('Cannot set date to a past day.')


class Task(models.Model):
    PRIORITIES = (
        (0, "None"),
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
    )

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=0, choices=PRIORITIES)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def _str_(self):
        return self.title

    class Meta:
       abstract = True


class CalendarTask(Task):
    date = models.DateField(blank=False, null=False, validators=[validate_date])


class InboxTask(Task):
    pass


class DeletedTask(Task):
    deletion_date = models.DateField(blank=False, null=False)