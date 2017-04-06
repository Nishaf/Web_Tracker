from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator,EmailValidator
from Images.models import PostImages,ExcelFiles


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = ExcelFiles
        fields = [
            "username",
            "timestamp",
            "filee",
        ]


def hasNumbers(name):
    return any(char.isdigit() for char in name)

def validate_name(value):
    if hasNumbers(value):
        raise forms.ValidationError("Name Should not contain any Numbers")

class UserForm(forms.ModelForm):
    first_name = forms.CharField(validators=[validate_name])
    last_name = forms.CharField(validators=[validate_name])
    email = forms.EmailField(validators=[EmailValidator])
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email','date_joined']



class ImageForm(forms.ModelForm):
    class Meta:
        model = PostImages
        fields = [
            "username",
            "timestamp",
            "sector",
            "image"
        ]




