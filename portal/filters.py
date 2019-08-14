import django_filters

#
# class LavagemFilter(django_filters.FilterSet):
#     data__gte = django_filters.DateFilter(field_name='data', lookup_expr='gte', label='Data inicial')
#     data__lte = django_filters.DateFilter(field_name='data', lookup_expr='lte', label='Data final')
#     consumo__gte = django_filters.NumberFilter(field_name='consumo', lookup_expr='gte', label='Consumo')
#     consumo__lte = django_filters.NumberFilter(field_name='consumo', lookup_expr='lte', label='Consumo')
#
#     # class Meta:
#     #     model = Lavagem
#     #     fields = ['data', 'filtro', 'consumo']
#
#
