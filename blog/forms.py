from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post


class UserRegistrationForm(forms.ModelForm):
    """
    Simple user registration form
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        # Chek if user password and confirm password are same
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


class CommentForm(forms.ModelForm):
    """
    Simple comment form
    """
    class Meta:
        model = Comment
        fields = ('name', 'body')


class PostForm(forms.ModelForm):
    """
    Simple post form
    """
    class Meta:
        model = Post
        fields = ('title', 'body')
