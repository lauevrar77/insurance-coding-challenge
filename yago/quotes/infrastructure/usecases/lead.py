from quotes.models import LeadContact, Enterprise
from django.http import HttpRequest
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateLeadCommand:
    firstname: str
    lastname: str
    address: str
    phone: str
    email: str
    legal_name: str
    enterprise_number: str
    natural_person: bool
    annual_revenue: float

    @classmethod
    def from_request(cls, request: HttpRequest):
        annual_revenue = request.POST.get("annual_revenue", 0)
        if not annual_revenue:
            raise ValueError("Annual revenue is required")
        return cls(
            firstname=request.POST["firstname"],
            lastname=request.POST["lastname"],
            address=request.POST["address"],
            phone=request.POST["phone"],
            email=request.POST["email"],
            legal_name=request.POST["legal_name"],
            enterprise_number=request.POST["enterprise_number"],
            natural_person=bool(request.POST.get("natural_person", False)),
            annual_revenue=float(request.POST.get("annual_revenue", 0)),
        )


class LeadUseCase:
    def create(self, cmd: CreateLeadCommand) -> tuple[LeadContact, Enterprise]:
        lead = LeadContact(
            firstname=cmd.firstname,
            lastname=cmd.lastname,
            address=cmd.address,
            phone=cmd.phone,
            email=cmd.email,
        )
        lead.full_clean()
        lead.save()

        enterprise = Enterprise(
            legal_name=cmd.legal_name,
            enterprise_number=cmd.enterprise_number,
            natural_person=bool(cmd.natural_person),
            annual_revenue=float(cmd.annual_revenue),
        )
        enterprise.full_clean()
        enterprise.save()

        return lead, enterprise
