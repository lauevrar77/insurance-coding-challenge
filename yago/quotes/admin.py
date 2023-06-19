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


class NacebelCodeAdmin(admin.ModelAdmin):
    list_display = ["level", "code", "label_fr"]
    list_filter = ["level"]
    search_fields = ["label_fr"]


admin.site.register(NacebelCode, NacebelCodeAdmin)


class CoverAdviceInline(admin.StackedInline):
    model = NacebelCodeCoverAdvice
    extra = 1


class NacebelCodeAdviceAdmin(admin.ModelAdmin):
    list_display = ["nacebel_code"]
    search_fields = ["nacebel_code"]
    inlines = [CoverAdviceInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(NacebelCodeAdviceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["nacebel_code"].queryset = NacebelCode.objects.filter(level=5)
        return form


admin.site.register(NacebelCodeAdvice, NacebelCodeAdviceAdmin)


class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ["legal_name", "enterprise_number"]
    search_fields = ["legal_name", "enterprise_number"]


admin.site.register(Enterprise, EnterpriseAdmin)


class CoverPremiumInline(admin.StackedInline):
    model = CoverPremium
    extra = 0


class SimulatedQuoteAdmin(admin.ModelAdmin):
    list_display = ["remote_quote_id"]
    search_fields = ["remote_quote_id"]
    inlines = [CoverPremiumInline]


admin.site.register(SimulatedQuote, SimulatedQuoteAdmin)


class AdvicedCoverInline(admin.StackedInline):
    model = AdvicedCover
    extra = 0


class QuoteSimulationAdmin(admin.ModelAdmin):
    list_display = ["lead_contact", "enterprise", "reviewed"]
    search_fields = ["lead_contact", "enterprise"]
    inlines = [AdvicedCoverInline]
    list_filter = ["reviewed"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuoteSimulationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["codes"].queryset = NacebelCode.objects.filter(level=5)
        return form


admin.site.register(QuoteSimulation, QuoteSimulationAdmin)


class QuoteSimulationInline(admin.StackedInline):
    model = QuoteSimulation
    extra = 0


class LeadContactAdmin(admin.ModelAdmin):
    list_display = ["firstname", "lastname", "phone", "email"]
    search_fields = ["firstname", "lastname", "phone", "email"]
    inlines = [QuoteSimulationInline]


admin.site.register(LeadContact, LeadContactAdmin)
