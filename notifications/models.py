from django.db import models
from accounts.models import Account
from jobs.models import Job
from posts.models import Post

# Create your models here.

class Notification(models.Model):

    receiver = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    sender = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        null=True,
        blank=True
    )

    message = models.CharField(max_length=255)

    notification_type = models.CharField(
        max_length=50
    )

    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )