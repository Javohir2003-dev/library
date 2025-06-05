from django.db import models
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.validators import MinLengthValidator,MinValueValidator,MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey


from user.models import Costom_User





# Category model -------------------------------------------------

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya")
    slug = models.SlugField(max_length=150, unique=True, blank=True, verbose_name="Slug")
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Ota-ona"
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        indexes = [
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_children(self):
        return self.children.all()


# End Category model -------------------------------------------------


# Kitob model -------------------------------------------------

def secure_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    safe_name = slugify(name) 
    return f"uploads/{safe_name}{ext}" 


def save(self, *args, **kwargs):
    self.name = self.name.lower()
    self.author = self.author.lower()
    super().save(*args, **kwargs)


class Kitob(models.Model):
    name = models.CharField(max_length=200, verbose_name='Kitob_nomi')
    author = models.CharField(max_length=100, verbose_name='Muallif')
    publication_year =  models.PositiveIntegerField(verbose_name="Nashr_yili")
    language = models.CharField(max_length=50,
        choices=[("uz", "O'zbek"), ('ru', 'Rus'),('en', 'Ingliz')], 
        default="uz", 
        verbose_name="Til"
        )
    description = models.TextField("Tavsif", blank=True, null=True)
    image = models.ImageField(upload_to='kitob_rasmlari/', blank=True, null=True, verbose_name='Kitob rasmi')
    file = models.FileField(upload_to='kitoblar/',verbose_name="Yuklangan fayl")
    views = models.PositiveBigIntegerField(default=0, verbose_name="Ko'rganlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kitoblar',
        verbose_name="Kategorya"
    ) 


    class Meta:
        indexes = [
            models.Index(fields=['name', 'author']),
        ]
        unique_together = ['name', 'author', 'publication_year']
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"



@receiver(post_delete, sender=Kitob)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

# End Kitob model -------------------------------------------------




# Like model -------------------------------------------------

class Like(models.Model):
    user = models.ForeignKey(Costom_User, on_delete=models.CASCADE, related_name='kitob_likes', verbose_name="Foydalanuvchi")
    kitob = models.ForeignKey(Kitob, on_delete=models.CASCADE, related_name='likes', verbose_name="Kitob")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Layk qo'yilgan sana")

    class Meta:
        verbose_name = "Layk"
        verbose_name_plural = "Layklar"
        unique_together = [['user', 'kitob']]  # Bir foydalanuvchi bir kitobga faqat bitta layk qo'yadi
        indexes = [
            models.Index(fields=['user', 'kitob']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.kitob.name} uchun layk"

# Like model -------------------------------------------------



# Comment model -------------------------------------------------

class Comment(models.Model):
    kitob = models.ForeignKey(Kitob, on_delete=models.CASCADE, related_name='comments', verbose_name="Kitob")
    user = models.ForeignKey(Costom_User, on_delete=models.CASCADE, related_name='kitob_comments', verbose_name="Foydalanuvchi")
    text = models.TextField(
        verbose_name="Komment",
        validators=[MinLengthValidator(2, message="Komment kamida 2 ta belgidan iborat bo'lishi kerak.")]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Komment"
        verbose_name_plural = "Kommentlar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['kitob', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.kitob.name} uchun komment"

# End Comment model -------------------------------------------------



# Cart model -------------------------------------------------

class Cart(models.Model):
    user = models.OneToOneField(Costom_User, on_delete=models.CASCADE, related_name='cart', verbose_name="Foydalanuvchi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Savat"
        verbose_name_plural = "Savatlar"

    def __str__(self):
        return f"{self.user.username} savati"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Savat")
    kitob = models.ForeignKey(Kitob, on_delete=models.CASCADE, verbose_name="Kitob")


    class Meta:
        verbose_name = "Savat elementi"
        verbose_name_plural = "Savat elementlari"
        unique_together = [['cart', 'kitob']]  # Bir savatda bir kitob faqat bir marta
        indexes = [
            models.Index(fields=['cart', 'kitob']),
        ]

    def __str__(self):
        return f"{self.kitob.name} ({self.quantity} dona)"
    
# End Cart model -------------------------------------------------





