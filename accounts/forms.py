from django import forms
from .models import Profile


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


def validate_pw_length(value):
    if len(value) < 10:
        raise forms.ValidationError('New password must be at least 10 characters.')


def validate_pw_no_username(value, username):
    if username.lower() in value.lower():
        raise forms.ValidationError('Password must not include your username.')


def validate_pw_no_first_name(value, first_name):
    if first_name.lower() in value.lower():
        raise forms.ValidationError('Password must not include your first name.')


def validate_pw_no_last_name(value, last_name):
    if last_name.lower() in value.lower():
        raise forms.ValidationError('Password must not include your last name.')


# New password
# TODO both uppercase and lowercase letters
# TODO One or more numerical digits
# TODO One or more special characers # $ @
class ChangePasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(
        widget=forms.PasswordInput()
        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
        )

    def clean_new_password(self):
        new_pw = self.cleaned_data.get('new_password')
        username = self.user.get_username()
        first_name = self.user.profile.first_name
        last_name = self.user.profile.last_name
        validate_pw_length(new_pw)
        validate_pw_no_username(new_pw, username)
        validate_pw_no_first_name(new_pw, first_name)
        validate_pw_no_last_name(new_pw, last_name)
        return new_pw

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password', '')
        new_password = cleaned_data.get('new_password', '')
        confirm_password = cleaned_data.get('confirm_password', '')
        if new_password != confirm_password:
            raise forms.ValidationError('Passwords don\'t match! Please make sure you confirm your new password.')
        
        if current_password == new_password:
            raise forms.ValidationError('Your new password can\'t be the same as your old password!')