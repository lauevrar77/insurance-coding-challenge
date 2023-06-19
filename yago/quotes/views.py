from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from quotes.infrastructure.persistance.views.nacebel_codes import NacebelCodeView
from quotes.infrastructure.persistance.views.suggestions import SuggestionView
from quotes.infrastructure.services.insurer import InsurerService
from quotes.infrastructure.usecases.lead import CreateLeadCommand, LeadUseCase
from quotes.infrastructure.usecases.quote import (
    QuoteUseCase,
    SaveSimulationCommand,
    SimulateQuoteCommand,
)
from quotes.models import QuoteAdvice, QuoteSimulation

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    codes_tree = NacebelCodeView().all_as_tree()
    return render(request, "quotes/index.html", {"codes": codes_tree})


def get_simulate_quote_command(
    request: HttpRequest, codes: list[str], advice: QuoteAdvice
) -> SimulateQuoteCommand:
    return SimulateQuoteCommand(
        int(request.POST["annual_revenue"]),
        request.POST["enterprise_number"],
        request.POST["legal_name"],
        bool(request.POST.get("natural_person", False)),
        codes,
        advice.deductible_formula,
        advice.coverage_ceiling_formula,
    )


def submit_quote(request: HttpRequest) -> HttpResponse:
    insurer_service = InsurerService(
        settings.INSURER_ENDPOINT,
        settings.INSURER_API_KEY,
    )
    lead_usecase = LeadUseCase()
    code_view = NacebelCodeView()
    quote_usecase = QuoteUseCase(insurer_service, code_view)
    suggestion_view = SuggestionView()

    # TODO : better form errors handling

    try:
        codes = codes_from_request(request)
        lead, enterprise = lead_usecase.create(CreateLeadCommand.from_request(request))
        advice = suggestion_view.suggestion_for_codes(codes)
        simulated_quote = quote_usecase.simulate(
            get_simulate_quote_command(request, codes, advice)
        )
        simulation = quote_usecase.save_simulation(
            SaveSimulationCommand(simulated_quote, enterprise, lead, codes, advice)
        )
    except (ValidationError, ValueError) as e:
        codes_tree = code_view.all_as_tree()
        return render(
            request,
            "quotes/index.html",
            {
                "codes": codes_tree,
                "error_messages": e.message_dict
                if isinstance(e, ValidationError)
                else {"Annual revenue": [str(e)]},
            },
        )

    return HttpResponseRedirect(reverse("quote_result", args=(simulation.uuid,)))


def codes_from_request(request: HttpRequest) -> list[str]:
    codes = []
    for key in request.POST.keys():
        if key.startswith("code-"):
            code = key.split("-")[1]
            codes.append(code)
    if len(codes) == 0:
        raise ValidationError({"codes": ["Please select at least one code"]})
    return codes


def quote_result(request: HttpRequest, simulation_uuid: str) -> HttpResponse:
    # TODO : Add this in a view ?
    simulation = get_object_or_404(QuoteSimulation, uuid=simulation_uuid)
    return render(request, "quotes/result.html", {"simulation": simulation})
