import django_filters
from django import forms
from .models import Training, CatCity, CatTrainingType


class TrainingFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # type__name = django_filters.CharFilter(field_name='type__name', lookup_expr='icontains',
    #                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = django_filters.ModelChoiceFilter(
        queryset=CatTrainingType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        label='Training Type'

    )

    city = django_filters.ModelChoiceFilter(queryset=CatCity.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control form-select'}))

    date_start = django_filters.DateFilter(field_name='date_start', lookup_expr='gte',
                                           widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_end = django_filters.DateFilter(field_name='date_end', lookup_expr='lte',
                                         widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Training
        fields = ['name', 'type', 'city', 'date_start', 'date_end']
