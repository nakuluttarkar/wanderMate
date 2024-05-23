from django import forms
from .models import Preference, PreferenceOption

class PreferenceForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(
        queryset=PreferenceOption.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Preference
        fields = ['preferences']
