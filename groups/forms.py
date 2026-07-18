from .models import Group, GroupRequest, GroupPost, GroupComment
from django import forms


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['owner','members']

    def __init__(self,*args,**kwargs):
        super(GroupForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = '__all__'
        exclude = ['group','user']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share something with the group...'
            })
        }

    def __init__(self,*args,**kwargs):
        super(GroupPostForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})




class GroupCommentForm(forms.ModelForm):
    class Meta:
        model = GroupComment
        fields = ['content']

    def __init__(self,*args,**kwargs):
        super(GroupCommentForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})