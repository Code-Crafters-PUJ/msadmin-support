from django.db import models

# Create your models here.


class Clients(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    company_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=20)
    nit = models.IntegerField()
    status = models.BooleanField(default=True)


class PQR(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    PETICION = "Peticion"
    QUEJA = "Queja"
    RECLAMO = "Reclamo"

    TIPO_SOLICITUD_CHOICES = [
        (PETICION, "Peticion"),
        (QUEJA, "Queja"),
        (RECLAMO, "Reclamo"),
    ]

    tipo_solicitud = models.CharField(max_length=20, choices=TIPO_SOLICITUD_CHOICES)

    RECIBIDO = "Recibido"
    EN_PROCESO = "En proceso"
    CERRADO = "Cerrado"

    ESTADO_CHOICES = [
        (RECIBIDO, "Recibido"),
        (EN_PROCESO, "En proceso"),
        (CERRADO, "Cerrado"),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_solicitud = models.DateTimeField()
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField()
    id_cliente = models.ForeignKey(Clients, on_delete=models.CASCADE)


class respuestas_solicitudes(models.Model):
    historial_solicitudes_id = models.IntegerField(primary_key=True)
    pqrs_empresa_id = models.ForeignKey(PQR, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField()
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField()
