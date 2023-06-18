from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from quotes.forms import QuoteForm
from quotes.infrastructure.persistance.views.nacebel_codes import NacebelCodeView

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    codes_tree = NacebelCodeView().all_as_tree()
    form = QuoteForm()
    return render(request, "quotes/index.html", {"codes": codes_tree, "form": form})
