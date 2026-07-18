from django.db import models
from accounts.models import Account

# Create your models here.

class Group(models.Model):
    owner = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='owned_groups')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='groups',default='default.jpg')
    members = models.ManyToManyField(Account,blank=True,related_name='joined_groups')
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def members_count(self):
        return self.members.count()

    def __str__(self):
        return self.name
    

class GroupRequest(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='group_requests')
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='join_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.full_name} - {self.group.name}'
    


class GroupPost(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='group_posts')
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='groups',null=True,blank=True)
    likes = models.ManyToManyField(
        Account,
        blank=True,
        related_name='liked_group_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.content[:50]
    


class GroupComment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    post = models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:50]