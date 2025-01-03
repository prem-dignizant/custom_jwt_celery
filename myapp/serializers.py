from rest_framework import serializers
from .models import Buyer , BuyerToken
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta


def generate_buyer_token(buyer):
    refresh = RefreshToken.for_user(buyer)
    access_token = refresh.access_token
    # Set expiration time
    access_token.set_exp(lifetime=timedelta(days=1))
    refresh.set_exp(lifetime=timedelta(days=7))
    # Save token details in the database

    buyer_token = BuyerToken.objects.filter(buyer=buyer).first()
    if buyer_token:
        buyer_token.refresh_token = str(refresh)
        buyer_token.access_token = str(access_token)
        buyer_token.expires_at = datetime.now() + timedelta(days=7)
        buyer_token.save()
    else:
        BuyerToken.objects.create(
            buyer=buyer,
            refresh_token=str(refresh),
            access_token=str(access_token),

            expires_at=datetime.now() + timedelta(days=7),
        )


    return {"refresh": str(refresh),"access": str(access_token)}

class BuyerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            buyer = Buyer.objects.get(email=email)
        except Buyer.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password")

        if password != buyer.password:
            raise AuthenticationFailed("Invalid email or password")

        # Generate tokens
        tokens = generate_buyer_token(buyer)
        return {
            'refresh': tokens['refresh'],
            'access': tokens['access'],
            
        }