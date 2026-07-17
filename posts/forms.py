from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user','likes','shared_by','shared_post','shared_body','views','tags']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'Create New Post...',
                'style': 'width: 100%;border-button: 3px solid #ccc;'
            })
        }

    def __init__(self,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['user','post']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Say Something...'
            })
        }

    def __init__(self,*args,**kwargs):
        super(CommentForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


    
class SharePostForm(forms.Form):
    shared_body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'input'
            }
        )
    )