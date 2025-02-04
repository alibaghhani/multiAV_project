from django.db import models


class CommonItems(models.Model):
    RESULT_CHOICES = (
        (1, 'infected'),
        (0, 'Clean'),
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True