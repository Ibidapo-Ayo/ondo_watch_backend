# Create your views here.

from rest_framework import generics

from .models import OdourReport
from .serializers import OdourReportSerializer
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from .filters import OdourReportFilter

from rest_framework.throttling import AnonRateThrottle;

class OdourReportThrottle(AnonRateThrottle):
    scope = "odour_report"

class OdourReportPagination(PageNumberPagination):
    page_size = 10

class OdourReportListCreateView(generics.ListCreateAPIView):
    throttle_classes = [OdourReportThrottle]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = OdourReportFilter
    
    
    def get_queryset(self):
        queryset = OdourReport.objects.all().order_by("-reported_at")
        
        return queryset
    serializer_class = OdourReportSerializer
    pagination_class = OdourReportPagination
