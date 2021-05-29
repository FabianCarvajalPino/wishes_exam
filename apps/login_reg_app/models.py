from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print(postData)
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not NAME_REGEX.match(postData['first_name']) or len(postData['first_name'])<2:
            errors['first_name'] = "Nombre invalido, se admiten solo letras y debe tener al menos 2 caracteres"
        if not NAME_REGEX.match(postData['last_name']) or len(postData['last_name'])<2:
            errors['last_name'] = "Apellido invalido, se admiten solo letras y debe tener al menos 2 caracteres"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Correo con formato invalido"
        for user in User.objects.all():
            if postData['email'].lower() == user.email.lower():
                errors['email2'] = "El correo que intentas registrar ya existe"
        if len(postData['password'])<8 or postData['password']!=postData['re_password']:
            errors['password'] = "Contraseña invalida, debe tener al menos 8 caracteres o no coincide con la repeticion"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Correo invalido"
        if len(postData['password'])<8:
            errors['password'] = "Contraseña invalida, debe tener al menos 8 caracteres"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    hash_pw = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()