from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_add_discount_to_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='capacity',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                verbose_name='Capacidad máxima (cupos)',
                help_text='Deja vacío para cupos ilimitados',
            ),
        ),
        migrations.AddField(
            model_name='package',
            name='booked_count',
            field=models.PositiveIntegerField(
                default=0,
                verbose_name='Reservas activas',
                help_text='Se actualiza automáticamente con cada reserva confirmada',
            ),
        ),
    ]
