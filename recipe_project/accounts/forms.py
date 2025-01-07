from django import forms
from .models import CustomUser, UserProfile

#A resistration form for a new user extending django's form.

class Register(forms.ModelForm):
    class Meta:
        model = CustomUser

        fields = [
            'username',
            'email',
            'password',
        ]
        widgets = {'password':forms.PasswordInput()}

#Form for updating a users Username and email.
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

#Form for updating a user's profile picture.
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']