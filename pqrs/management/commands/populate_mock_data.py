from django.core.management.base import BaseCommand
from django.utils import timezone

from pqrs.models import PQR, respuestas_solicitudes


class Command(BaseCommand):
    help = "Populate the database with mock data"

    def handle(self, *args, **options):
        pqr_instance = PQR.objects.create(
            empresa_id=1,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.CERRADO,
            fecha_solicitud=timezone.now(),
            asunto="Visualización",
            descripcion="Los usuarios no pueden visualizar la información de la empresa",
        )

        # Create an instance of respuestas_solicitudes for testing
        respuestas_solicitudes.objects.create(
            historial_solicitudes_id=1,
            pqrs_empresa_id=pqr_instance,
            fecha_respuesta=timezone.now(),
            asunto="Res: Visualización",
            descripcion="Se ha solucionado el problema de visualización",
        )

        PQR.objects.create(
            empresa_id=2,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.EN_PROCESO,
            fecha_solicitud=timezone.now(),
            asunto="Error al iniciar sesión",
            descripcion="Algunos usuarios no pueden iniciar sesión",
        )

        PQR.objects.create(
            empresa_id=4,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.RECIBIDO,
            fecha_solicitud=timezone.now(),
            asunto="Creación de cuenta",
            descripcion="No se puede crear una cuenta en la plataforma",
        )

        pqr_instance2 = PQR.objects.create(
            empresa_id=10,
            tipo_solicitud=PQR.PETICION,
            estado=PQR.RECLAMO,
            fecha_solicitud=timezone.now(),
            asunto="Monto erróneo",
            descripcion="El monto de la factura es incorrecto",
        )

        respuestas_solicitudes.objects.create(
            historial_solicitudes_id=2,
            pqrs_empresa_id=pqr_instance2,
            fecha_respuesta=timezone.now(),
            asunto="Res: Monto erróneo",
            descripcion="Concidere revisar la factura nuevamente",
        )

        self.stdout.write(self.style.SUCCESS("Successfully populated mock data"))
