from django import forms
from blog.models import Profile


class SubscribeForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email',)


class UnsubscribeForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email',)


class ContactForm(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 22, 'cols': 10}))
