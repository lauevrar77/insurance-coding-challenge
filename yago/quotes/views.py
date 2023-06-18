from quotes.models import (
    LeadContact,
    Enterprise,
    QuoteSimulation,
    NacebelCode,
    SimulatedQuote,
    CoverPremium,
    AdvicedCover,
)
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from quotes.infrastructure.persistance.views.nacebel_codes import NacebelCodeView
from quotes.infrastructure.persistance.views.suggestions import SuggestionView
from quotes.infrastructure.services.insurer import GetQuoteCommand, InsurerService

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    codes_tree = NacebelCodeView().all_as_tree()
    return render(request, "quotes/index.html", {"codes": codes_tree})


def submit_quote(request: HttpRequest) -> HttpResponse:
    print(request.POST)
    codes = codes_from_request(request)
    lead = LeadContact(
        firstname=request.POST.get("firstname"),
        lastname=request.POST.get("lastname"),
        address=request.POST.get("address"),
        phone=request.POST.get("phone"),
        email=request.POST.get("email"),
    )
    lead.full_clean()
    lead.save()

    enterprise = Enterprise(
        legal_name=request.POST.get("legal_name"),
        enterprise_number=request.POST.get("enterprise_number"),
        natural_person=bool(request.POST.get("natural_person", False)),
        annual_revenue=float(request.POST.get("annual_revenue", 0)),
    )
    enterprise.full_clean()
    enterprise.save()

    advice = SuggestionView().suggestion_for_codes(codes)

    insurer = InsurerService(
        "https://staging-gtw.seraphin.be", "fABF1NGkfn5fpHuJHrbvG3niQX6A1CO53ftF9ASD"
    )
    insurer_quote = insurer.get_quote(
        GetQuoteCommand(
            int(request.POST["annual_revenue"]),
            request.POST["enterprise_number"],
            request.POST["legal_name"],
            bool(request.POST.get("natural_person", False)),
            codes,
        )
    )

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

    simulation = QuoteSimulation(
        enterprise=enterprise,
        lead_contact=lead,
        deductible_formula=advice.deductible_formula,
        coverage_ceiling_formula=advice.coverage_ceiling_formula,
    )
    simulation.simulated_quote = simulated_quote
    simulation.full_clean()
    simulation.save()
    for cover in advice.covers:
        adviced_cover = AdvicedCover(
            cover=cover,
            quote=simulation,
        )
        adviced_cover.full_clean()
        adviced_cover.save()

    for code in NacebelCodeView().from_codes(codes):
        simulation.codes.add(code)
    simulation.simulated_quote = simulated_quote
    simulation.save()

    return HttpResponseRedirect(reverse("quote_result", args=(simulation.uuid,)))


def codes_from_request(request: HttpRequest) -> list[str]:
    codes = []
    for key, value in request.POST.items():
        if key.startswith("code-"):
            code = key.split("-")[1]
            codes.append(code)
    return codes


def quote_result(request: HttpRequest, simulation_uuid: str) -> HttpResponse:
    simulation = get_object_or_404(QuoteSimulation, uuid=simulation_uuid)
    return render(request, "quotes/result.html", {"simulation": simulation})
