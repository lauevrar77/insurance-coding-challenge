from dataclasses import dataclass

from quotes.infrastructure.persistance.views.nacebel_codes import NacebelCodeView
from quotes.infrastructure.services.insurer import (
    GetQuoteCommand,
    InsurerService,
    Quote,
)
from quotes.models import (
    AdvicedCover,
    CoverPremium,
    Enterprise,
    LeadContact,
    QuoteAdvice,
    QuoteSimulation,
    SimulatedQuote,
)


@dataclass(frozen=True)
class SimulateQuoteCommand:
    annual_revenue: int
    enterprise_number: str
    legal_name: str
    natural_person: bool
    nacebel_codes: list[str]
    deductible_formula: str
    coverage_ceiling_formula: str


@dataclass(frozen=True)
class SaveSimulationCommand:
    simulated_quote: SimulatedQuote
    enterprise: Enterprise
    lead_contact: LeadContact
    codes: list[str]
    advice: QuoteAdvice


class QuoteUseCase:
    def __init__(
        self, insurer_service: InsurerService, code_view: NacebelCodeView
    ) -> None:
        self.__insurer_service = insurer_service
        self.__code_view = code_view

    def save_simulation(self, cmd: SaveSimulationCommand) -> QuoteSimulation:
        simulation = QuoteSimulation(
            enterprise=cmd.enterprise,
            lead_contact=cmd.lead_contact,
            deductible_formula=cmd.advice.deductible_formula,
            coverage_ceiling_formula=cmd.advice.coverage_ceiling_formula,
        )
        simulation.simulated_quote = cmd.simulated_quote
        simulation.full_clean()
        simulation.save()
        for cover in cmd.advice.covers:
            adviced_cover = AdvicedCover(
                cover=cover,
                quote=simulation,
            )
            adviced_cover.full_clean()
            adviced_cover.save()

        for code in self.__code_view.from_codes(cmd.codes):
            simulation.codes.add(code)
        simulation.simulated_quote = cmd.simulated_quote
        simulation.save()
        return simulation

    def simulate(self, cmd: SimulateQuoteCommand) -> SimulatedQuote:
        insurer_quote = self.__simulate_quote(cmd)
        simulated_quote = SimulatedQuote(
            available=insurer_quote.available,
            coverage_ceiling=insurer_quote.coverage_ceiling,
            deductible=insurer_quote.deductible,
            remote_quote_id=insurer_quote.quote_id,
        )
        simulated_quote.full_clean()
        simulated_quote.save()

        for gross in insurer_quote.gross_premiums:
            cover = CoverPremium(
                cover=gross.cover,
                premium=gross.premium,
                quote=simulated_quote,
            )
            cover.full_clean()
            cover.save()
        return simulated_quote

    def __simulate_quote(self, cmd: SimulateQuoteCommand) -> Quote:
        insurer_quote = self.__insurer_service.get_quote(
            cmd=GetQuoteCommand(
                enterprise_number=cmd.enterprise_number,
                legal_name=cmd.legal_name,
                nacebel_codes=cmd.nacebel_codes,
                deductible_formula=cmd.deductible_formula,
                coverage_ceiling_formula=cmd.coverage_ceiling_formula,
                annual_revenue=cmd.annual_revenue,
                natural_person=cmd.natural_person,
            )
        )
        return insurer_quote
