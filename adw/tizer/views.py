from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
from tizer.models import Wallet, Tizer, Transaction
from tizer.serializers import TizerSerializer
from rest_framework.response import Response
from tizer.process import Process
from rest_framework import status

User = get_user_model()


class TizerListApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    # 1. List all
    def get(self, request, *args, **kwargs):
        tizer = Tizer.objects.all()
        serializer = TizerSerializer(tizer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Update tizer
    def post(self, request, *args, **kwargs):
        err = ""
        try:
            tizer: Tizer = Tizer.objects.get(id=request.data['id'])
            tizer_status = Tizer.Status(request.data['status'])
        except:
            err = "Invalid request"
            req_status = status.HTTP_400_BAD_REQUEST
        else:
            if Process(tizer, tizer_status, self.request.user).run():
                req_status = status.HTTP_200_OK
            else:
                err = "Invalid request"
                req_status = status.HTTP_400_BAD_REQUEST
        return Response(err, status=req_status)
