from django.db import models


class TimeEntry(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ('end_time',)

    def hours(self):
        delta = self.end_time - self.start_time

        hours_rounded = 0
        total_seconds = delta.total_seconds()
        while total_seconds > 7.5 * 60:
            hours_rounded += .25
            total_seconds -= 15 * 60

        return hours_rounded
