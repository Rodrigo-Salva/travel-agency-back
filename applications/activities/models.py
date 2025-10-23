from django.db import models

# Create your models here.

class Activity(models.Model):
    class ActivityType(models.TextChoices):
        SIGHTSEEING = 'sightseeing', 'Sightseeing'
        ADVENTURE = 'adventure', 'Adventure'
        CULTURAL = 'cultural', 'Cultural'
        SHOPPING = 'shopping', 'Shopping'
        DINING = 'dining', 'Dining'
        SPORTS = 'sports', 'Sports'
        WELLNESS = 'wellness', 'Wellness'
        ENTERTAINMENT = 'entertainment', 'Entertainment'

    class DifficultyLevel(models.TextChoices):
        EASY = 'easy', 'Easy'
        MODERATE = 'moderate', 'Moderate'
        DIFFICULT = 'difficult', 'Difficult'

    name = models.CharField(max_length=100)
    destination = models.ForeignKey('destinations.Destination', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    description = models.TextField()
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1) 
    difficulty_level = models.CharField(max_length=10, choices=DifficultyLevel.choices)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    max_group_size = models.PositiveIntegerField()
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'actividades'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.activity_type})"
