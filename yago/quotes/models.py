from django.db import models
import uuid


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

    @property
    def covers(self) -> list["NacebelCodeCoverAdvice"]:
        return list(self.cover_advices.all())


class NacebelCodeCoverAdvice(models.Model):
    nacebel_code_advice = models.ForeignKey(
        NacebelCodeAdvice, on_delete=models.CASCADE, related_name="cover_advices"
    )
    cover = models.CharField(max_length=255)


class QuoteAdvice:
    def __init__(self, quote_code_advices: list[NacebelCodeAdvice]):
        self.__advices: list[NacebelCodeAdvice] = quote_code_advices

    @property
    def coverage_ceiling_formula(self) -> str:
        if not self.__advices:
            return "S"
        values = ["S", "L"]
        max_index = -1
        for advice in self.__advices:
            max_index = max(max_index, values.index(advice.coverageCeilingFormula))
        return values[max_index]

    @property
    def deductible_formula(self) -> str:
        if not self.__advices:
            return "M"

        values = ["S", "M", "L"]
        max_index = -1
        for advice in self.__advices:
            max_index = max(max_index, values.index(advice.deductibleFormula))
        return values[max_index]

    @property
    def covers(self) -> list[str]:
        return list(
            {
                cover_advice.cover
                for advice in self.__advices
                for cover_advice in advice.covers
            }
        )


class LeadContact(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()


class Enterprise(models.Model):
    legal_name = models.CharField(max_length=255)
    enterprise_number = models.CharField(max_length=255)
    natural_person = models.BooleanField()
    annual_revenue = models.FloatField()


class SimulatedQuote(models.Model):
    available = models.BooleanField()
    coverage_ceiling = models.FloatField()
    deductible = models.FloatField()
    remote_quote_id = models.CharField(max_length=255)


class CoverPremium(models.Model):
    cover = models.CharField(max_length=255)
    premium = models.FloatField()
    quote = models.ForeignKey(
        SimulatedQuote, on_delete=models.CASCADE, related_name="covers"
    )


class QuoteSimulation(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    lead_contact = models.ForeignKey(LeadContact, on_delete=models.CASCADE)
    codes = models.ManyToManyField(NacebelCode)
    deductible_formula = models.CharField(
        max_length=2, choices=[("S", "Small"), ("M", "Medium"), ("L", "Large")]
    )
    coverage_ceiling_formula = models.CharField(
        max_length=2, choices=[("S", "Small"), ("L", "Large")]
    )
    simulated_quote = models.ForeignKey(SimulatedQuote, on_delete=models.CASCADE)


class AdvicedCover(models.Model):
    cover = models.CharField(max_length=255)
    quote = models.ForeignKey(
        QuoteSimulation, on_delete=models.CASCADE, related_name="adviced_covers"
    )
