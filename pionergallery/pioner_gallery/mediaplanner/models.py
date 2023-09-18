from django.db import models
from django.urls import reverse

class Marker(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='marker_images/')


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start_time.isoformat(),
            'end': self.end_time.isoformat(),
            'url': reverse('event_detail', args=[self.id]),
        }
