from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import FilterSet


class VacancyFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
