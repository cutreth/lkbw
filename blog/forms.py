from django import forms
from blog.models import Profile


class UnsubscribeForm(forms.ModelForm):



    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email',)
