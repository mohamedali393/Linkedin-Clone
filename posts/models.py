from django.db import models
from accounts.models import Account
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts',null=True,blank=True)
    content = models.TextField()
    shared_by = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='shared_posts',null=True,blank=True)
    shared_post = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='shares',
        null=True,
        blank=True
    )
    shared_body = models.TextField(blank=True)
    likes = models.ManyToManyField(Account,blank=True,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(
        default=0
    )
    
    @property
    def get_url(self):
        return reverse('post-detail',args=[self.pk])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:50]
    

class Comment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_parent(self):
        return self.parent == None
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_at')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:50]