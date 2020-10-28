from django.db import models


class CreatedAndUpdatedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CodeModel(models.Model):

    code = models.CharField(unique=True, max_length=255)

    class Meta:
        abstract = True
