from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    confirm_email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'date_of_birth', 'email']
