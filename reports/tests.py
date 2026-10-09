from django.test import SimpleTestCase

from .serializers import OdourReportSerializer


class OdourReportSerializerTests(SimpleTestCase):
    def test_intensity_is_included_in_response_fields(self):
        field = OdourReportSerializer().fields["intensity"]

        self.assertFalse(field.write_only)
