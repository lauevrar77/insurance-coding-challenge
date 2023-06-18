from django.contrib import admin

# Register your models here.
from quotes.models import (
    NacebelCode,
    NacebelCodeAdvice,
    NacebelCodeCoverAdvice,
    LeadContact,
    Enterprise,
    SimulatedQuote,
    CoverPremium,
    QuoteSimulation,
    AdvicedCover,
)

admin.site.register(NacebelCode)
admin.site.register(NacebelCodeAdvice)
admin.site.register(NacebelCodeCoverAdvice)
admin.site.register(LeadContact)
admin.site.register(Enterprise)
admin.site.register(SimulatedQuote)
admin.site.register(CoverPremium)
admin.site.register(QuoteSimulation)
admin.site.register(AdvicedCover)
