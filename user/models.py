from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver









# User model

class CustomUser(AbstractUser):
    phone = models.CharField(
        max_length=15,
        verbose_name='Telefon raqam',
        validators=[
            RegexValidator(
                regex=r'^\+998\d{9}$',
                message="Telefon raqami to'g'ri formatda kiritilishi kerak. Masalan, +998901234567"
            )
        ]

    )

    def __str__(self):
        return f"{self.username} {self.phone}"





# User profile model

class Profile(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ism")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Familiya")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Manzil')
    image = models.ImageField(upload_to='profile_rasmlari/', blank=True, null=True, verbose_name='Profile rasmlari')
    bio = models.TextField(verbose_name="Biografiya", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Tug'ulgan sana", blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Aniqlanmagan')],
        default='unknown',
        verbose_name='Jins'
    )

    def __str__(self):
        return f"{self.user.phone} -- profile"

    def save(self, *args, **kwargs):
        try:
            old_instance = Profile.objects.get(pk=self.pk)
        except Profile.DoesNotExist:
            old_instance = None

        if old_instance:
            self._changed_fields = {
                'image': str(old_instance.image) != str(self.image),
                'bio': old_instance.bio != self.bio,
                'birth_date': old_instance.birth_date != self.birth_date,
            }
        else:
            self._changed_fields = {}

        super().save(*args, **kwargs)

    def has_changed(self):
        return any(self._changed_fields.values()) if hasattr(self, '_changed_fields') else False


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)