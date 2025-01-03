from django.db import models

# Create your models here.


class Buyer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)  # Store hashed passwords!
    
    def __str__(self):
        return self.email
    


class BuyerToken(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="tokens")
    refresh_token = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return str(self.buyer)