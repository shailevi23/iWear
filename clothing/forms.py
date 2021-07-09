from django.utils import timezone
from django import forms
from clothing.models import ClothingItem, WornEvent
from users.models import User

class ItemCreationForm(forms.ModelForm):
    name = forms.CharField(label='Item Name')
    owner = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all())

    class Meta:
        model = ClothingItem
        fields = ('name', 'owner', 'category', 'tag_id','image_url')


class WornEventCreationForm(forms.ModelForm):
    item = forms.ModelChoiceField(ClothingItem.objects.all())

    class Meta:
        model = WornEvent
        fields = ('item',)

class WornEventCreationForm(forms.Form):
    tag_id = forms.CharField()


class WeatherRangeForm(forms.Form):
    minimum_temperature = forms.IntegerField(min_value=-15)
    maximum_temperature = forms.IntegerField(max_value=45)
