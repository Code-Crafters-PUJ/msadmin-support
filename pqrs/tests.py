from django.test import TestCase, Client
from django.urls import reverse
from .models import Clients, PQR, PetitionResponses
from django.utils import timezone
import json

class PQRViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client_1 = Clients.objects.create(id=1, company_name="Test Company", email="test@example.com", status=True, nit="123456789")
        self.pqr_1 = PQR.objects.create(id=1, client=self.client_1, state="Recibido",petition_date=timezone.now(),subject="Test Subject 1",description="Test Description 1")
        self.pqr_2 = PQR.objects.create(id=2, client=self.client_1, state="Cerrado",petition_date=timezone.now(),subject="Test Subject 2",description="Test Description 2")

    def test_allPQRview_no_auth(self):
        response = self.client.get(reverse('pqrs:pqr'))
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"message": "You must include an Authorization header"})

    def test_singleClientPQRview_no_auth(self):
        response = self.client.get(reverse('pqrs:pqr_client', kwargs={'pk': self.client_1.id}))
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"message": "You must include an Authorization header"})

    def test_ManagePQRview_post_no_auth(self):
        response = self.client.post(reverse('pqrs:manage_pqr', kwargs={'pk': self.pqr_1.id}), data=json.dumps({
            "subject": "Test Subject",
            "description": "Test Description"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"message": "You must include an Authorization header"})

    def test_singleClientView_get_no_auth(self):
        response = self.client.get(reverse('pqrs:client_pqr', kwargs={'pk': self.client_1.id}))
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"message": "You must include an Authorization header"})

    def test_singleClientView_delete_no_auth(self):
        response = self.client.delete(reverse('pqrs:client_pqr', kwargs={'pk': self.client_1.id}))
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"message": "You must include an Authorization header"})
