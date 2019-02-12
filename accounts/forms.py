from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    confirm_email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'date_of_birth', 'email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', None)
        confirm_email = cleaned_data.get('confirm_email', None)
        # If either the email or confirm email is provided make sure they are equal
        if email is not None or confirm_email is not None:
            if email != confirm_email:
                raise forms.ValidationError('Emails must match!')
