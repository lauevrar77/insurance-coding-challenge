from django.db import models


# Create your models here.
class NacebelCode(models.Model):
    level = models.IntegerField()
    code = models.CharField(max_length=5)
    parent_code = models.CharField(max_length=5)
    label_fr = models.CharField(max_length=255)
    label_nl = models.CharField(max_length=255)
    label_en = models.CharField(max_length=255)
    label_de = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.label_fr} ({self.pk})"


class NacebelCodeAdvice(models.Model):
    nacebel_code = models.ForeignKey(NacebelCode, on_delete=models.DO_NOTHING)
    deductibleFormula = models.CharField(
        max_length=255, choices=[("S", "Small"), ("M", "Medium"), ("L", "Large")]
    )
    coverageCeilingFormula = models.CharField(
        max_length=255, choices=[("S", "Small"), ("L", "Large")]
    )


class NacebelCodeCoverAdvice(models.Model):
    nacebel_code_advice = models.ForeignKey(NacebelCodeAdvice, on_delete=models.CASCADE)
    cover = models.CharField(max_length=255)
