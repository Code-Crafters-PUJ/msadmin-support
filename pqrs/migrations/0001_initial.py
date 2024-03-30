# Generated by Django 4.2.7 on 2024-03-30 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PQR",
            fields=[
                (
                    "empresa_id",
                    models.IntegerField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "tipo_solicitud",
                    models.CharField(
                        choices=[
                            ("Peticion", "Peticion"),
                            ("Queja", "Queja"),
                            ("Reclamo", "Reclamo"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("Recibido", "Recibido"),
                            ("En proceso", "En proceso"),
                            ("Cerrado", "Cerrado"),
                        ],
                        max_length=20,
                    ),
                ),
                ("fecha_solicitud", models.DateTimeField()),
                ("asunto", models.CharField(max_length=100)),
                ("descripcion", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="respuestas_solicitudes",
            fields=[
                (
                    "historial_solicitudes_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("fecha_respuesta", models.DateTimeField()),
                ("asunto", models.CharField(max_length=100)),
                ("descripcion", models.TextField()),
                (
                    "pqrs_empresa_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pqrs.pqr"
                    ),
                ),
            ],
        ),
    ]
