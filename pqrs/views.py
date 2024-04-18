import json
from typing import Any

import jwt
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from config.settings import SECRET_KEY
from pqrs.rabbitmq import get_rabbitmq_connection

from .models import PQR, PetitionResponses


def send_jwt_validation_request(token: str) -> None:
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Define el mensaje que enviarás, puede ser cualquier información necesaria para la validación
    message: dict[str, Any] = {"token": token}

    # Publica el mensaje en la cola
    channel.basic_publish(
        exchange="", routing_key="jwt_validation_queue", body=json.dumps(message)
    )

    connection.close()


def validate_role(token: str, role: str) -> bool:
    payload: dict[str, Any]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(payload)
    except jwt.InvalidTokenError:
        return False

    if payload["role"] != role:
        return False
    return True


def validate_admin_role(token: str) -> bool:
    return validate_role(token, "ADMIN")


def validate_soporte_role(token: str) -> bool:
    return validate_role(token, "SOPORTE")


class allPQRview(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        # token: str | None = request.headers.get("Authorization")

        # if not token:
        #     return JsonResponse(
        #         {"message": "You must include an Authorization header"}, status=401
        #     )

        # if not (validate_admin_role(token) or validate_soporte_role(token)):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        pqrs = PQR.objects.values()
        return JsonResponse({"pqrs": list(pqrs)}, safe=False)

    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> JsonResponse:
        # token: str | None = request.headers.get("Authorization")

        # if not token:
        #     return JsonResponse(
        #         {"message": "You must include an Authorization header"}, status=401
        #     )

        jd = json.loads(request.body)
        # send_jwt_validation_request(token)

        try:
            # if not (validate_admin_role(token) or validate_soporte_role(token)):
            #     return JsonResponse(
            #         {"message": "You don't have the required permissions"}, status=403
            #     )

            PQR.objects.create(
                tipo_solicitud=jd["tipo_solicitud"],
                state=PQR.EN_PROCESO,
                petition_type=PQR.PETICION,
                subject=jd["asunto"],
                description=jd["descripcion"],
                petition_date=timezone.now(),
                client=jd["client_id"],
            )
            return JsonResponse({"message": "PQR created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


class singlePQRview(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        # token: str | None = request.headers.get("Authorization")

        # if not token:
        #     return JsonResponse(
        #         {"message": "You must include an Authorization header"}, status=401
        #     )

        # if not (validate_admin_role(token) or validate_soporte_role(token)):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        pqr = PQR.objects.filter(empresa_id=pk).values()
        return JsonResponse({"pqr": list(pqr)}, safe=False)


class ManagePQRview(View):
    def post(self, request: HttpRequest, pk: int) -> JsonResponse:
        # token: str | None = request.headers.get("Authorization")

        jd = json.loads(request.body)

        # if not token:
        #     return JsonResponse(
        #         {"message": "You must include an Authorization header"}, status=401
        #     )

        # if not (validate_admin_role(token) or validate_soporte_role(token)):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        response_request: PetitionResponses

        try:
            response_request = PetitionResponses.objects.create(
                id=pk,
                tipo_solicitud=jd["tipo_solicitud"],
                estado=jd["estado"],
                fecha_solicitud=jd["fecha_solicitud"],
                asunto=jd["asunto"],
                descripcion=jd["descripcion"],
            )
        except Exception:
            return JsonResponse(
                {
                    "message": "tipo_solicitud, estado, fecha_solicitud, asunto and descripcion are required"
                },
                status=400,
            )

        return JsonResponse(
            {"message": "PQR created successfully", "response": response_request},
            status=201,
        )
