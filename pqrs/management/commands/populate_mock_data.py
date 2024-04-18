from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from pqrs.models import PQR, Clients, respuestas_solicitudes


class Command(BaseCommand):
    help = "Populate the database with mock data"

    def handle(self, *args: Any, **options: Any):
        empresa_1 = Clients.objects.create(
            id=1,
            company_name="Empresa 1",
            contact_name="Empresa 1",
            nit=123456789,
            email="empresa1@gmail.com",
            telephono="1234567",
        )

        empresa_2 = Clients.objects.create(
            id=1,
            company_name="Empresa 2",
            contact_name="Empresa 2",
            nit=123456789,
            email="empresa2@gmail.com",
            telephono="1234567",
        )

        empresa_3 = Clients.objects.create(
            id=1,
            company_name="Empresa 3",
            contact_name="Empresa 3",
            nit=123456789,
            email="empresa3@gmail.com",
            telephono="1234567",
        )

        pqr_instance = PQR.objects.create(
            id=1,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.CERRADO,
            fecha_solicitud=timezone.now(),
            asunto="Visualización",
            descripcion="Los usuarios no pueden visualizar la información de la empresa",
            id_cliente=empresa_1,
        )

        # Create an instance of respuestas_solicitudes for testing
        respuestas_solicitudes.objects.create(
            historial_solicitudes_id=1,
            pqrs_id=pqr_instance,
            fecha_respuesta=timezone.now(),
            asunto="Res: Visualización",
            descripcion="Se ha solucionado el problema de visualización",
        )

        PQR.objects.create(
            id=2,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.EN_PROCESO,
            fecha_solicitud=timezone.now(),
            asunto="Error al iniciar sesión",
            descripcion="Algunos usuarios no pueden iniciar sesión",
            id_cliente=empresa_2,
        )

        PQR.objects.create(
            id=4,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.RECIBIDO,
            fecha_solicitud=timezone.now(),
            asunto="Creación de cuenta",
            descripcion="No se puede crear una cuenta en la plataforma",
            id_cliente=empresa_3,
        )

        pqr_instance2 = PQR.objects.create(
            id=10,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.RECLAMO,
            fecha_solicitud=timezone.now(),
            asunto="Monto erróneo",
            descripcion="El monto de la factura es incorrecto",
            id_cliente=empresa_2,
        )

        respuestas_solicitudes.objects.create(
            historial_solicitudes_id=2,
            pqrs_id=pqr_instance2,
            fecha_respuesta=timezone.now(),
            asunto="Res: Monto erróneo",
            descripcion="Concidere revisar la factura nuevamente",
        )

        self.stdout.write(self.style.SUCCESS("Successfully populated mock data"))
