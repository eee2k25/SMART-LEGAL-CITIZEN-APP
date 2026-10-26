from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Feedback


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True, label="Full name")
    terms = forms.BooleanField(
        required=True, label="I accept the terms and privacy notice"
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")

    def clean_email(self):
        value = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return value

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.email = self.cleaned_data["email"]
        obj.first_name = self.cleaned_data["first_name"]
        if commit:
            obj.save()
        return obj


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if (
            User.objects.filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("This email is already in use.")
        return email


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("category", "subject", "message", "email")
        widgets = {
            "category": forms.Select(
                choices=[
                    ("site", "Website"),
                    ("content", "Legal information"),
                    ("accessibility", "Accessibility"),
                    ("other", "Other"),
                ]
            )
        }
