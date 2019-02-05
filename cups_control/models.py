import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CupOwner(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    mail = models.EmailField()

    def __str__(self):
        return self.name + ' ' + self.surname


class Cup(models.Model):
    owner = models.ForeignKey(CupOwner, on_delete=models.CASCADE)
    last_marked = models.DateTimeField('Last rebuke')
    rebukes_count = models.IntegerField(default=0)
    is_dirty = models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner) + '\' ' + 'cup'

    def should_be_removed(self):
        return self.rebukes_count > 2

    def reset_rebuke_count(self):
        self.rebukes_count = 0
        self.save()

    def increase_rebuke_count(self):
        self.rebukes_count += 1
        self.last_marked = timezone.now()
        self.save()

    def mark_as_dirty(self):
        self.is_dirty = True

    def is_dirty(self):
        return self.is_dirty

    def can_be_rebuked(self):
        return timezone.now() >= self.last_marked + timezone.timedelta(days=1)


class Event(models.Model):
    event_type = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cup_owner')
    event_performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_performer")
    event_time = models.TimeField(default=timezone.now)




