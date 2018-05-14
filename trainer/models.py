from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ToxicComments(models.Model):

    TOXIC_CHOICES = {
        (0, "Toxic"),
        (1, "Not Toxic"),
    }

    profile_id = models.CharField(max_length=255)
    post_id = models.CharField(max_length=255)
    comment_user_id = models.CharField(max_length=255)
    comment_text = models.TextField()
    comment_time = models.TextField()
    toxicity = models.IntegerField(choices=TOXIC_CHOICES)

    def __unicode__(self):
        return self.post_id