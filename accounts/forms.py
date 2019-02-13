from django import forms
from .models import Profile
from datetime import datetime
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'date_of_birth', 'email']

    confirm_email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(
        required=False,
        widget = forms.DateInput(format='%m/%d/%Y'),
        input_formats=('%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d')
    )

    def clean_bio(self):
        data = self.cleaned_data.get('bio', None)
        if data and len(data) < 10:
            raise forms.ValidationError('Bio must be at least 10 characters.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', None)
        confirm_email = cleaned_data.get('confirm_email', None)
        # If either the email or confirm email is provided make sure they are equal
        if email is not None or confirm_email is not None:
            if email != confirm_email:
                raise forms.ValidationError('Emails must match!')


class ResetPasswordForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['password']

    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())