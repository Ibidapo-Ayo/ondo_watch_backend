from django.urls import path

from .views import OdourReportListCreateView


urlpatterns = [
    path(
        "reports/",
        OdourReportListCreateView.as_view(),
        name="odour-report-list-create",
    ),
]   