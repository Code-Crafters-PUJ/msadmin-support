from django.db import models

# Create your models here.


class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=20)
    nit = models.IntegerField()
    status = models.BooleanField(default=True)


class PQR(models.Model):
    id = models.AutoField(primary_key=True)

    PETICION = "Peticion"
    QUEJA = "Queja"
    RECLAMO = "Reclamo"

    PETITION_TYPE_CHOICES = [
        (PETICION, "Peticion"),
        (QUEJA, "Queja"),
        (RECLAMO, "Reclamo"),
    ]

    petition_type = models.CharField(max_length=20, choices=PETITION_TYPE_CHOICES)

    RECIBIDO = "Recibido"
    EN_PROCESO = "En proceso"
    CERRADO = "Cerrado"

    STATE_CHOICES = [
        (RECIBIDO, "Recibido"),
        (EN_PROCESO, "En proceso"),
        (CERRADO, "Cerrado"),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    petition_date = models.DateTimeField()
    subject = models.CharField(max_length=100)
    description = models.TextField()
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)


class PetitionResponses(models.Model):
    id = models.AutoField(primary_key=True)
    pqr = models.ForeignKey(PQR, on_delete=models.CASCADE)
    response_date = models.DateTimeField()
    subject = models.CharField(max_length=100)
    description = models.TextField()
