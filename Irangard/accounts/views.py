import requests
import json
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from .models import StagedPayments, SpecialUser
from django.contrib.auth import authenticate, login
from accounts.serializers.payment_serializers import VerifiedPaymentSerializer


class PayViewSet(GenericViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = VerifiedPaymentSerializer

    # def get_serializer(self, *args, **kwargs):
    #     return None

    @action(detail=False, url_path='pay', methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    def pay(self, request):

        order_id = str(uuid.uuid4())
        my_data = {
            "order_id": order_id,
            "amount": 10000,
            "name": f"{request.user.username}",
            "mail": f"{request.user.email}",
            "callback": "http://188.121.123.141:8000/accounts/pay/verify/"
        }

        my_headers = {"Content-Type": "application/json",
                      'X-API-KEY': '3394842f-7407-4598-8c48-499a15c8d0b7',
                      'X-SANDBOX': '0'}

        response = requests.post(url="https://api.idpay.ir/v1.1/payment", data=json.dumps(my_data),
                                 headers=my_headers)
        response.raise_for_status()
        print(response.status_code)
        try:
            obj = StagedPayments.objects.get(user=request.user)
            obj.transaction_id = json.loads(response.content)['id']
            obj.order_id = order_id
            obj.save()

        except StagedPayments.DoesNotExist:
            obj = StagedPayments.objects.create(transaction_id=json.loads(response.content)[
                'id'], order_id=order_id, user=request.user)
            obj.save()
        except:
            return Response(f"bad request", status=status.HTTP_400_BAD_REQUEST)

        return Response(f"{json.loads(response.content)}", status=status.HTTP_200_OK)

    @action(detail=False, url_path='verify', methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    def verify(self, request):

        my_data = {
            "order_id": request.data['order_id'],
            "id": request.data['id'],

        }

        my_headers = {"Content-Type": "application/json",
                      'X-API-KEY': '3394842f-7407-4598-8c48-499a15c8d0b7',
                      'X-SANDBOX': '0'
                      }

        response = requests.post(url="https://api.idpay.ir/v1.1/payment/verify", data=json.dumps(my_data),
                                 headers=my_headers)
        response.raise_for_status()
        #print(response.content, ' ', response.status_code)

        if(response.status_code == 200):

            try:
                user = StagedPayments.objects.get(
                    transaction_id=request.data['id'])
                sp_user = SpecialUser.objects.create(user=user)
                sp_user.save()
                st_payment = StagedPayments.objects.get(user=user)
                st_payment.delete()
                return Response(f"{json.loads(response.content)}", status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(f"bad request", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(f"transaction is not verified", status=status.HTTP_405_METHOD_NOT_ALLOWED)
