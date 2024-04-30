import json
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import PQR, Clients, PetitionResponses

# from .helpers.jwt import validate_admin_role, validate_soporte_role



class allPQRview(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        token: str | None = request.headers.get("Authorization")

        if not token:
            return JsonResponse(
                {"message": "You must include an Authorization header"}, status=401
            )

        # if not (validate_admin_role(token) or validate_soporte_role(token)):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        pqrs = list(
            PQR.objects.select_related("Clients").filter(client__status=True).values()
        )
        return JsonResponse({"pqrs": pqrs}, safe=False)


class singleClientPQRview(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        token: str | None = request.headers.get("Authorization")

        if not token:
            return JsonResponse(
                {"message": "You must include an Authorization header"}, status=401
            )

        # if not (validate_admin_role(token) or validate_soporte_role(token)):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        try:
            client = Clients.objects.get(id=pk)
            if not client or not client.status:
                raise Clients.DoesNotExist

            pqr = list(PQR.objects.filter(client_id=pk).values())
            return JsonResponse({"pqr": pqr}, safe=False)
        except Clients.DoesNotExist:
            return JsonResponse(
                {"message": "client_id not found"},
                status=404,
            )


class ManagePQRview(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, pk: int) -> JsonResponse:
        token: str | None = request.headers.get("Authorization")

        if not token:
            return JsonResponse(
                {"message": "You must include an Authorization header"}, status=401
            )

        # if not validate_soporte_role(token):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        try:
            jd = json.loads(request.body)
            pqr = PQR.objects.get(id=pk)

            if pqr.client.status is False:
                return JsonResponse(
                    {"message": "Client is not active"},
                    status=400,
                )

            if pqr.state == PQR.CERRADO:
                return JsonResponse(
                    {"message": "PQR is already closed"},
                    status=400,
                )

            response_request = PetitionResponses.objects.create(
                pqr=pqr,
                response_date=timezone.now(),
                subject=jd["subject"],
                description=jd["description"],
            )

            pqr.state = PQR.CERRADO
            pqr.save()
            return JsonResponse(
                {
                    "message": "PQR closed successfully",
                    "response": {
                        "id": response_request.id,
                        "pqr_id": response_request.pqr.id,
                        "response_date": response_request.response_date,
                        "subject": response_request.subject,
                        "description": response_request.description,
                    },
                },
                status=201,
            )
        except PQR.DoesNotExist:
            return JsonResponse(
                {"message": "pqr_id not found"},
                status=404,
            )
        except (json.JSONDecodeError, KeyError):
            return JsonResponse(
                {"message": "subject and description are required"},
                status=400,
            )


class singleClientView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        token: str | None = request.headers.get("Authorization")

        if not token:
            return JsonResponse(
                {"message": "You must include an Authorization header"}, status=401
            )

        # if not (validate_admin_role(token) or validate_soporte_role(token)):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        try:
            client = list(Clients.objects.filter(id=pk, status=True).values())[0]
            return JsonResponse({"client": client}, safe=False)
        except (Clients.DoesNotExist, IndexError):
            return JsonResponse(
                {"message": "client_id not found"},
                status=404,
            )

    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        token: str | None = request.headers.get("Authorization")

        if not token:
            return JsonResponse(
                {"message": "You must include an Authorization header"}, status=401
            )

        # if not validate_admin_role(token):
        #     return JsonResponse(
        #         {"message": "You don't have the required permissions"}, status=403
        #     )

        try:
            client = Clients.objects.get(id=pk, status=True)
            client.status = False
            client.save()
        except Clients.DoesNotExist:
            return JsonResponse(
                {"message": "client_id not found"},
                status=404,
            )

        return JsonResponse({"message": "Client deleted successfully"}, status=200)
