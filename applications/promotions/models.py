from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from applications.authentication.models import User
from applications.packages.models import Package


class Coupon(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Porcentaje'),
        ('fixed', 'Monto fijo'),
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Código del cupón'
    )
    
    description = models.CharField(
        max_length=200,
        verbose_name='Descripción'
    )
    
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
        verbose_name='Tipo de descuento'
    )
    
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Valor del descuento'
    )
    
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Compra mínima'
    )
    
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Descuento máximo'
    )
    
    valid_from = models.DateField(
        verbose_name='Válido desde'
    )
    
    valid_until = models.DateField(
        verbose_name='Válido hasta'
    )
    
    max_uses = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Usos máximos'
    )
    
    times_used = models.IntegerField(
        default=0,
        verbose_name='Veces usado'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='¿Está activo?'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    class Meta:
        db_table = 'cupones'
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.discount_value}{'%' if self.discount_type == 'percentage' else '$'}"
    
    def get_discount_display(self):
        if self.discount_type == 'percentage':
            return f"{self.discount_value}%"
        return f"${self.discount_value}"
    
    def is_valid(self):
        today = timezone.now().date()
        if not self.is_active:
            return False
        if today < self.valid_from or today > self.valid_until:
            return False
        if self.max_uses and self.times_used >= self.max_uses:
            return False
        return True
    
    def can_be_used(self, purchase_amount):
        if not self.is_valid():
            return False
        if self.min_purchase_amount and purchase_amount < self.min_purchase_amount:
            return False
        return True
    
    def calculate_discount(self, purchase_amount):
        if not self.can_be_used(purchase_amount):
            return Decimal('0')
        
        if self.discount_type == 'percentage':
            discount = purchase_amount * (self.discount_value / Decimal('100'))
        else:
            discount = self.discount_value
        
        if self.max_discount_amount:
            discount = min(discount, self.max_discount_amount)
        
        return discount
    
    def use_coupon(self):
        self.times_used += 1
        self.save()


class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist',
        verbose_name='Usuario'
    )
    
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='wishlists',
        verbose_name='Paquete'
    )
    
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de agregado'
    )
    
    class Meta:
        db_table = 'lista_deseos'
        verbose_name = 'Lista de Deseos'
        verbose_name_plural = 'Listas de Deseos'
        ordering = ['-added_at']
        unique_together = ['user', 'package']
    
    def __str__(self):
        return f"{self.user.username} - {self.package.name}"