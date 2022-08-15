from dataclasses import field
import imp
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from engineerapp.models import *   #update i yarattıktan sonra kurduk

#forms sayesinde admin gibi kendi kendine alan yaratmadan viewsa çekerek form oluşturmuş oluyorsun modeldeki parametrelerle
class EngForms(forms.ModelForm):
    class Meta:
        model=EngModel
        fields="__all__"  #bu Engmodel altındaki tüm fieldları eng_id ve name i kapsıyor yani ??

class EngLPForms(forms.ModelForm):  
    class Meta:
        model = EngLPModel
        fields = "__all__"

class AccForm(forms.ModelForm):
    class Meta:
        model = AccreditationModel
        fields = "__all__"
    
class EngLPStepForms(forms.ModelForm):
    class Meta:
        model = EngLPStepModel
        fields = "__all__"
        exclude = ['completed',]    # I exclude it because, if we add the step we must be complete that necessity.

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] #confirmation pw 


class LPSForm(forms.ModelForm): #dynamic form denedim ama yine olmadı
    def __init__(self,learningpath,*args,**kwargs):
        super (LPSForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['lp_step'].queryset = LPStepsModel.objects.filter(learningpath=learningpath)
        self.fields['learningpath'].queryset = LPModel.objects.filter(learningpath=learningpath)

    class Meta:
        model = EngLPStepModel
        fields = "__all__"