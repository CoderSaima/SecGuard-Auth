from django.db import models

class SecAuth_Model(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


    def __str__(self):
        return f"User profile: {self.name} | Verified Email: {self.email}"