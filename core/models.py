from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from key_generator.key_generator import generate
import random

person_id_checker = RegexValidator(
    regex=r'^[0-9]*$',
    message="یک کد ملی معتبر وارد کنید."
)

credit_cart_checker = RegexValidator(
    regex=r'^[0-9]*$',
    message="یک شماره کارت معتبر وارد کنید."
)

postal_code_checker = RegexValidator(
    regex=r'^[0-9]*$',
    message="یک کدپستی معتبر وارد کنید."
)


def validate_phone_number(value):
    if value and is_number(value) and\
            is_valid_phone_number(value) and\
            len(value) == 11:
        return value
    else:
        raise ValidationError("یک شماره تلفن معتبر وارد کنید.")


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_valid_phone_number(number):
    if number[0] == '0' and number[1] == '9':
        return True
    else:
        return False


def key_generator():
    seed = random.randint(0, 1e100)
    key_custom = generate(5, '-', 4, 4, type_of_value='hex', capital='none', seed=seed).get_key()
    return key_custom


def create_new_ref_number():
    return str(random.randint(1000000000, 9999999999))


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password,
                    **extra_fields):
        """Create and save a new user"""
        if phone_number and \
                is_number(phone_number) and \
                is_valid_phone_number(phone_number) and \
                len(phone_number) == 11:
            pass
        else:
            raise ValueError('Phone number is invalid!')

        # email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password):
        """create and save new super user"""
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support email instead of username"""
    phone_number = models.CharField(
        validators=[validate_phone_number],
        max_length=11,
        unique=True,
    )
    name = models.CharField(max_length=255, null=True)
    generated_token = models.IntegerField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'


class Device(models.Model):
    deviceMac = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.deviceMac


class License(models.Model):
    CHOICES = (
        ('trial', 'Trial'),
        ('time limit', 'Time Limit'),
    )
    key = models.CharField(max_length=24, default=key_generator, unique=True, editable=False)
    created_on = models.DateField(auto_now_add=True, editable=False)
    expired_on = models.DateField()
    deviceNumber = models.IntegerField(default=1)
    devices = models.ManyToManyField(Device, related_name='devices', blank=True)
    licenseType = models.CharField(max_length=255, choices=CHOICES)
    name = models.CharField(max_length=255, default=0000, null=True)
    phone = models.CharField(max_length=255, default=0000, null=True)
    email = models.EmailField(max_length=255, null=True)
    education = models.CharField(max_length=255, default=0000, blank=True)
    job = models.CharField(max_length=255, default=0000, blank=True)
    active = models.BooleanField(default=False)
    serialNumber = models.CharField(max_length=255, default=create_new_ref_number, unique=True, editable=False)

    def __str__(self):
        return self.key
