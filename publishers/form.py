from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordResetForm
from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Section, Publisher, Article,Sections


class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields=["first_name","last_name","email","username","password1", "password2"]


class EditUserForm(forms.ModelForm):
    class Meta:
        model= User
        fields=("first_name","last_name","email","username")

class EditPublisherForm(forms.ModelForm):
    class Meta:
        model= Publisher
        fields=("section","description")

class ArticleCreationForm(forms.Form):
    """ArticleForm definition."""
    # TODO: Define form fields here
    title = forms.CharField(max_length=156)
    title_slug=forms.SlugField()
    description= forms.CharField(max_length=255,widget=forms.Textarea)
    keywords= forms.CharField(max_length=255,widget=forms.Textarea)
                            

class ArticleModelForm(forms.ModelForm):
    """Form definition for ArticleModel."""
    class Meta:
        """Meta definition for ArticleModelform."""
        model = Article
        fields = ('title','title_slug','image','image_source','image_description','sub_heading','body_text')
        
class ReferenceForm(forms.ModelForm):
    """Form definition for ArticleModel."""
    class Meta:
        """Meta definition for ArticleModelform."""
        model = Article
        fields = ("references", )



class SectionForm(forms.ModelForm):
    """Form definition for Section."""
    class Meta:
        """Meta definition for Sectionform."""
        model = Sections
        fields = ('Sub_section_image','image_source','image_description','sub_heading','body_text')
    
    

class PublishArticleForm(forms.ModelForm):
    """Form definition for PublishArticleForm."""

    class Meta:
        """Meta definition for PublishArticleFormform."""

        model = Article
        fields = ('publish',)
