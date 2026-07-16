from django import forms
from .models import Profile, Skill, Education, Experience

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','views']

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs.update({'class': 'input'})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(SkillForm,self).__init__(*args,**kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs.update({'class': 'input'})


        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
        exclude = ['user']

    def __init__(self,*args,**kwargs):
        super(EducationForm,self).__init__(*args,**kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs.update({'class': 'input'})



class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        exclude = ['user']

    def __init__(self,*args,**kwargs):
        super(ExperienceForm,self).__init__(*args,**kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs.update({'class': 'input'})