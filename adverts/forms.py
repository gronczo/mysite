from django import forms
from django.contrib.auth.models import *
from adverts import models

class AdvertForm(forms.ModelForm):
    class Meta:
        model = models.Advert
        fields = ('subcategory','title','description','price','city','contact')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = models.Subcategory

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password')

class LoginForm(forms.Form):
    #class Meta:
    #    model = User
    #    fields = ('username','password')
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class AttachmentForm(forms.ModelForm):
    #file = forms.FileField()
    class Meta:
        model = models.Attachment
        fields = ('file',)
