from django.db import models
import uuid
# Create your models here.

class CreatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True,)
    visible = models.BooleanField(default=True)

    def soft_delete(self):
        """soft  delete a model instance"""
        self.visible=False
        self.save()

    class Meta:
        abstract = True
        ordering = ['-created_at']

class EqChoice(models.IntegerChoices):
        CPU = 1, "CPU"
        HDD = 2, "HARDRIVE"
        RAM = 3, "RAM"

class EquipmentCatalog(CreatedModel):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    description = models.CharField(max_length=254)
    type = models.PositiveIntegerField(choices=EqChoice.choices, default=EqChoice.CPU)
    alias = models.CharField(max_length=200)

class ServiceEquipment(CreatedModel):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    type_equipment = models.ForeignKey(EquipmentCatalog, on_delete=models.DO_NOTHING)
    code=models.CharField(max_length=20, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['code']),
        ]

class Temps(CreatedModel):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    value = models.PositiveIntegerField(default=0)
    service_equipment = models.ForeignKey(ServiceEquipment, null=True,on_delete=models.DO_NOTHING)

