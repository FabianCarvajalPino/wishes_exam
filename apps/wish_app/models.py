from django.db import models
from django.db.models.fields import related
from ..login_reg_app.models import User
# Create your models here.

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['wish']) < 4:
            errors['wish'] = "El deseo debe contener al menos 3 caracteres"
        if len(postData['description'])<4:
            errors['description'] = "La descripcion es obligatoria y debe tener al menos 3 caracteres"
        return errors

class Wish(models.Model):
    wisher = models.ForeignKey(User, related_name='wishes_made', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='wishes_liked')
    wish = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    granted = models.BooleanField()
    date_granted = models.DateField(auto_now=True)
    objects = WishManager()