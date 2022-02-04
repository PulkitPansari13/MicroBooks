from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


def phone_validator(phno):
    errormsg = 'Enter a valid 10 digit phone number'
    if len(phno) != 10 or not phno.isdigit():
        raise ValidationError(errormsg)


class User(models.Model):
    first_name = models.CharField(max_length=75, blank=False, null=False)
    last_name = models.CharField(max_length=75, blank=False, null=False)
    email_id = models.EmailField(unique=True)
    phno = models.CharField(max_length=10, blank=False, null=False, unique=True, validators=[phone_validator])
