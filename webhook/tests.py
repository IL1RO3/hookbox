from datetime import timedelta

from django.test import SimpleTestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from webhook.serializers import EndpointSerializer


class EndpointSerializerExpirationDateTests(SimpleTestCase):
    def setUp(self):
        self.serializer = EndpointSerializer()

    def test_accepts_future_expiration_date(self):
        expiration_date = timezone.now() + timedelta(minutes=1)

        self.assertEqual(
            self.serializer.validate_expiration_date(expiration_date),
            expiration_date,
        )

    def test_rejects_past_expiration_date(self):
        expiration_date = timezone.now() - timedelta(minutes=1)

        with self.assertRaises(ValidationError):
            self.serializer.validate_expiration_date(expiration_date)

    def test_accepts_no_expiration_date(self):
        self.assertIsNone(self.serializer.validate_expiration_date(None))
