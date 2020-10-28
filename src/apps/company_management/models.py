from django.db import models

from src.utils.Utils import Utility
from src.utils.enums import Prefix
from src.utils.common_model import CodeModel, CreatedAndUpdatedModel


class Company(CodeModel, CreatedAndUpdatedModel):

    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)
        Utility.generate_code(Company, Prefix.COMPANY.value, self.id)

    def __str__(self):
        return self.name
