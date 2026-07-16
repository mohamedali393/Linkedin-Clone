from django.db import models
from accounts.models import Account

# Create your models here.

class Conversation(models.Model):
    participants = models.ManyToManyField(Account,related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation #{self.id}'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.first_name} {self.content[:50]}'