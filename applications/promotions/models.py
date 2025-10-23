from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Porcentaje'),
        ('fixed', 'Monto Fijo'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    description = models.CharField(max_length=200, verbose_name='Descripción')
    
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        verbose_name='Tipo de Descuento'
    )
    
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Valor del Descuento'
    )
    
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Monto Mínimo de Compra',
        null=True,
        blank=True
    )
    
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Descuento Máximo',
        null=True,
        blank=True
    )
    
    valid_from = models.DateField(verbose_name='Válido Desde')
    valid_until = models.DateField(verbose_name='Válido Hasta')
    
    max_uses = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Usos Máximos',
        null=True,
        blank=True
    )
    
    times_used = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Veces Usado'
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    
    class Meta:
        db_table = 'cupones'
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active', 'valid_from', 'valid_until']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.get_discount_display()}"
    
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
            return 0
        
        if self.discount_type == 'percentage':
            discount = purchase_amount * (self.discount_value / 100)
        else:
            discount = self.discount_value
        
        if self.max_discount_amount:
            discount = min(discount, self.max_discount_amount)
        
        return discount
    
    def use_coupon(self):
        self.times_used += 1
        self.save()