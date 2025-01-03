from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BuyerLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BuyerToken , Buyer
from rest_framework.decorators import api_view

class BuyerLoginView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        serializer = BuyerLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedBuyerView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        access_token = request.headers.get('Authorization')
        access_token = access_token.replace('Bearer ', '')
        try:
            buyer = BuyerToken.objects.get(access_token=access_token)
        except BuyerToken.DoesNotExist:
            return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": f"Hello, authenticated {buyer.buyer.email}!"})
    

class BuyerLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        access_token = request.headers.get('Authorization')
        access_token = access_token.replace('Bearer ', '')
        try:
            buyertoken = BuyerToken.objects.get(access_token=access_token)
        except BuyerToken.DoesNotExist:
            return Response({"message": "User not exist with this token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        buyertoken.delete()
        return Response({"message": "Logout successful!"})
    

from myapp.tasks import demo_task

@api_view(["GET"])
def demo_celery(request):
    result = demo_task.delay()
    print(result.id)
    # print(result.status)
    return Response({"message": "Hello, Celery!"})