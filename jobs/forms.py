from .models import Company, Job, JobApplication
from django import forms


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['owner']

    def __init__(self,*args,**kwargs):
        super(CompanyForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})




class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['user','company']

    def __init__(self,*args,**kwargs):
        super(JobForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = '__all__'
        exclude = ['job','user','status']

    def __init__(self,*args,**kwargs):
        super(JobApplicationForm,self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})