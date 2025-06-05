from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


    
# User model
class Costom_User(AbstractUser):
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Telefon',
        validators=[
            RegexValidator(
                regex=r'^\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{4,8}$',
                message="Telefon raqami to'g'ri formatda kiritilishi kerak. Masalan, +998 901 234567 yoki +998-901-234567"
        )
]
    )
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Manzil')
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'),('unknown', 'Aniqlanmagan')],
        default='unknown',
        verbose_name='Jins'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




# User profil model
class Profile(models.Model):
    user = models.OneToOneField(Costom_User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profil_rasmlari/', blank=True, null=True, verbose_name='Profil rasmi')
    bio = models.TextField(verbose_name="Biografiya", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Tug'ilgan sana", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profili"

    def save(self, *args, **kwargs):  # Eski qiymatlarni saqlash uchun
        if self.pk:
            old_instance = Profile.objects.get(pk=self.pk)
            self._changed_fields = {
                'image': old_instance.image != self.image,
                'bio': old_instance.bio != self.bio,
                'birth_date': old_instance.birth_date != self.birth_date,
            }
        else:
            self._changed_fields = {}
        super().save(*args, **kwargs)

    def has_changed(self):  # O'zgarish bor-yo'qligini tekshirish
        return any(self._changed_fields.values()) if hasattr(self, '_changed_fields') else False

@receiver(post_save, sender=Costom_User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    elif hasattr(instance, 'profile') and instance.profile.has_changed():
        instance.profile.save()
