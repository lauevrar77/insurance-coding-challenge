from ....models import NacebelCodeAdvice, QuoteAdvice


class SuggestionView:
    def suggestion_for_codes(self, codes: list[str]) -> QuoteAdvice:
        advices = list(
            NacebelCodeAdvice.objects.filter(nacebel_code__code__in=codes).all()
        )
        return QuoteAdvice(advices)
