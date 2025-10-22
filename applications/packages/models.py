from django.db import models

# Modelo creado para que los FK funcionen correctamente
class Package(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name


class PackagePlaceholder(models.Model):
	"""Small placeholder model to allow FK resolution during development."""
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Package placeholder'
		verbose_name_plural = 'Package placeholders'
