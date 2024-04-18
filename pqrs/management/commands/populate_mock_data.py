from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from pqrs.models import PQR, Clients, PetitionResponses


class Command(BaseCommand):
    help = "Populate the database with mock data"

    def handle(self, *args: Any, **options: Any):
        empresa_1 = Clients.objects.create(
            company_name="Empresa 1",
            contact_name="Empresa 1",
            nit=123456789,
            email="empresa1@gmail.com",
            telephone="1234567",
        )

        empresa_2 = Clients.objects.create(
            company_name="Empresa 2",
            contact_name="Empresa 2",
            nit=123456789,
            email="empresa2@gmail.com",
            telephone="1234567",
        )

        empresa_3 = Clients.objects.create(
            company_name="Empresa 3",
            contact_name="Empresa 3",
            nit=123456789,
            email="empresa3@gmail.com",
            telephone="1234567",
        )

        pqr_instance = PQR.objects.create(
            petition_type=PQR.PETICION,
            state=PQR.CERRADO,
            petition_date=timezone.now(),
            subject="Visualización",
            description="Los usuarios no pueden visualizar la información de la empresa",
            client=empresa_1,
        )

        # Create an instance of respuestas_solicitudes for testing
        PetitionResponses.objects.create(
            pqr=pqr_instance,
            response_date=timezone.now(),
            subject="Res: Visualización",
            description="Se ha solucionado el problema de visualización",
        )

        PQR.objects.create(
            petition_type=PQR.PETICION,
            state=PQR.EN_PROCESO,
            petition_date=timezone.now(),
            subject="Error al iniciar sesión",
            description="Algunos usuarios no pueden iniciar sesión",
            client=empresa_2,
        )

        PQR.objects.create(
            petition_type=PQR.PETICION,
            state=PQR.RECIBIDO,
            petition_date=timezone.now(),
            subject="Creación de cuenta",
            description="No se puede crear una cuenta en la plataforma",
            client=empresa_3,
        )

        pqr_instance2 = PQR.objects.create(
            petition_type=PQR.PETICION,
            state=PQR.RECLAMO,
            petition_date=timezone.now(),
            subject="Monto erróneo",
            description="El monto de la factura es incorrecto",
            client=empresa_2,
        )

        PetitionResponses.objects.create(
            pqr=pqr_instance2,
            response_date=timezone.now(),
            subject="Res: Monto erróneo",
            description="Concidere revisar la factura nuevamente",
        )

        self.stdout.write(self.style.SUCCESS("Successfully populated mock data"))
