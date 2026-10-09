import django_filters

from .models import OdourReport


class OdourReportFilter(django_filters.FilterSet):

    reported_after = django_filters.DateTimeFilter(
        field_name="reported_at",
        lookup_expr="gte",
    )

    reported_before = django_filters.DateTimeFilter(
        field_name="reported_at",
        lookup_expr="lte",
    )

    min_intensity = django_filters.NumberFilter(
        field_name="intensity",
        lookup_expr="gte",
    )

    max_intensity = django_filters.NumberFilter(
        field_name="intensity",
        lookup_expr="lte",
    )

    class Meta:
        model = OdourReport
        fields = [
            "intensity",
            "odour_type",
            "happening_now",
        ]