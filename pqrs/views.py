from django.shortcuts import render

from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config.settings import SECRET_KEY
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse

import jwt
import datetime
import json
import pika

from pqrs.rabbitmq import get_rabbitmq_connection


from .models import PQR


def send_jwt_validation_request(token):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Define el mensaje que enviarás, puede ser cualquier información necesaria para la validación
    message = {
        "token": token
    }

    # Publica el mensaje en la cola
    channel.basic_publish(
        exchange='', routing_key='jwt_validation_queue', body=json.dumps(message))

    connection.close()


class createPQRview(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        jd = json.loads(request.body)
        token = jd['token']
        #send_jwt_validation_request(token)
        try:
            PQR.objects.create(
                empresa_id=jd['empresa_id'],
                tipo_solicitud=jd['tipo_solicitud'],
                estado=jd['estado'],
                fecha_solicitud=jd['fecha_solicitud'],
                asunto=jd['asunto'],
                descripcion=jd['descripcion']
            )
            return JsonResponse({'message': 'PQR created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)



class getPQRview(View):
    def get(self, request, pk):
        pqr = PQR.objects.filter(empresa_id=pk).values()
        return JsonResponse({'pqr': list(pqr)}, safe=False)