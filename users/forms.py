from django import forms
from .models import User, Gender    

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput())
    birth_date = forms.DateField(label='Birth date [YYYY\MM\DD]')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'location', 'gender','birth_date', 'reader_id', 'image_url')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        min_length = 3

        if not password2:
            raise forms.ValidationError('You must confirm your password')
        if password1 != password2:
            raise forms.ValidationError('Your passwords do not match')
        if len(password1) < min_length:
            raise forms.ValidationError(f'Password must be at least {min_length} characters.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password must contain at least 1 digit.')
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError('Password must contain at least 1 letter.')
        return password2

    def save(self, commit=True):
        new_user = super(UserCreationForm, self).save(commit=False)
        new_user.set_password(self.cleaned_data["password1"])
        if commit:
            new_user.save()
        return new_user

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(label='Birth date [YYYY\MM\DD]')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'location', 'gender','birth_date', 'reader_id', 'image_url')


class GenderForm(forms.ModelForm):
    genders = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Gender.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="",
    )

    class Meta:
        model = User
        fields = ('genders',)
