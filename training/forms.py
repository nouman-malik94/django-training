from datetime import datetime

from django import forms
from .models import Training, ResourceItem, ResourcePerson, TrainingFile
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'type', 'date_start', 'date_end', 'city', 'street_address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': forms.Select(attrs={'class': 'form-control form-select'}),
            'city': forms.Select(attrs={'class': 'form-control form-select'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),

        }

class CustomClearableFileInput(ClearableFileInput):
    template_name = "training/clearable_file_input.html"
    hidden_fields = []

class TrainingFileForm(forms.ModelForm):
    class Meta:
        model = TrainingFile
        fields = ['description', 'file']

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            # 'file': forms.FileField(widget=CustomClearableFileInput),
            # 'file': forms.FileInput(attrs={'class': 'form-control'}),
            # 'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'file': CustomClearableFileInput(attrs={'class': 'form-control'})
            # 'file': forms.ClearableFileInput()
        }


class ResourcePersonForm(forms.ModelForm):
    class Meta:
        model = ResourcePerson
        # fields = '__all__'
        fields = ['name', 'dob', 'pin']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'dob': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'pin': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class ResourceItemForm(forms.ModelForm):
    class Meta:
        model = ResourceItem
        # fields = '__all__'
        fields = ['name', 'quantity', 'estimated_price']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'estimated_price': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


TrainingFileFormSet = inlineformset_factory(
    Training, TrainingFile, form=TrainingFileForm,
    extra=1
    # can_delete=False, can_delete_extra=True
)
ResourcePersonFormSet = inlineformset_factory(
    Training, ResourcePerson, form=ResourcePersonForm,
    extra=1
    # can_delete=False, can_delete_extra=True
)
ResourceItemFormSet = inlineformset_factory(
    Training, ResourceItem, form=ResourceItemForm,
    extra=1
    # can_delete=False, can_delete_extra=True
)
