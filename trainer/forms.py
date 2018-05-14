from django import forms

class ProfileForm(forms.Form):
    profile_id = forms.CharField(label="Profile Id", max_length= 255)

